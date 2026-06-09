from server.ranking_service import record_match_result, record_shot
from server.replay_service import add_fire_event, add_forfeit_event, finish_replay
from shared.message_type import (
    FIRE_RESULT,
    OPPONENT_FIRE_RESULT,
    SPECTATOR_UPDATE,
    GAME_OVER,
    TURN_UPDATE
)


def get_current_player_data(handler, room):
    current_player = room.get_player(handler.session_id)

    if current_player:
        return current_player

    return {
        "username": handler.username,
        "session_id": handler.session_id,
        "handler": handler
    }


def send_spectator_update(room, payload):
    for spectator in room.spectators:
        spectator_handler = spectator["handler"]
        spectator_handler.send(payload)


def handle_fire(handler, message):
    if not handler.room_id:
        handler.send_error("You are not in a room")
        return

    room = handler.matchmaking.room_manager.get_room(handler.room_id)

    if not room:
        handler.send_error("Room not found")
        return

    payload = message.get("payload", {})
    x = payload.get("x")
    y = payload.get("y")

    success, info, fire_data = room.fire(handler.session_id, x, y)

    if not success:
        handler.send_error(info)
        return

    record_shot(handler.username, fire_data["result"])

    add_fire_event(
        room_id=handler.room_id,
        shooter=handler.username,
        x=fire_data["x"],
        y=fire_data["y"],
        result=fire_data["result"],
        turn_number=fire_data["turn_number"]
    )

    opponent = room.get_opponent(handler.session_id)
    opponent_handler = opponent["handler"]

    handler.send({
        "type": FIRE_RESULT,
        "status": "OK",
        "room_id": handler.room_id,
        "payload": fire_data
    })

    opponent_handler.send({
        "type": OPPONENT_FIRE_RESULT,
        "status": "OK",
        "room_id": handler.room_id,
        "payload": fire_data
    })

    if len(room.players) >= 2:
        player_1 = room.players[0]
        player_2 = room.players[1]

        for spectator in room.spectators:
            spectator_handler = spectator["handler"]

            spectator_handler.send({
                "type": SPECTATOR_UPDATE,
                "status": "OK",
                "room_id": handler.room_id,
                "payload": {
                    "x": fire_data["x"],
                    "y": fire_data["y"],
                    "result": fire_data["result"],
                    "shooter_session_id": handler.session_id,
                    "target_session_id": opponent["session_id"],
                    "player_1_board": room.get_spectator_board(player_1["session_id"]),
                    "player_2_board": room.get_spectator_board(player_2["session_id"]),
                    "player_1_ships": room.get_ship_layout(player_1["session_id"]),
                    "player_2_ships": room.get_ship_layout(player_2["session_id"]),
                    "spectator_count": len(room.spectators),
                    "current_turn_session_id": room.current_turn,
                    "winner_session_id": fire_data["winner_session_id"]
                }
            })

    handler.logger.info(
        f"Room {handler.room_id}: {handler.username} fired at "
        f"({fire_data['x']}, {fire_data['y']}) = {fire_data['result']}"
    )

    if fire_data["winner_session_id"]:
        winner_player = room.get_player(fire_data["winner_session_id"])
        loser_player = room.get_opponent(fire_data["winner_session_id"])

        record_match_result(
            winner_username=winner_player["username"],
            loser_username=loser_player["username"]
        )

        finish_replay(
            room_id=handler.room_id,
            winner=winner_player["username"]
        )

        for player in room.players:
            player_handler = player["handler"]

            player_handler.send({
                "type": GAME_OVER,
                "status": "OK",
                "room_id": handler.room_id,
                "payload": {
                    "winner_session_id": fire_data["winner_session_id"]
                }
            })

        handler.logger.info(
            f"Game over in room {handler.room_id}. "
            f"Winner: {fire_data['winner_session_id']}"
        )
        return

    for player in room.players:
        player_handler = player["handler"]

        player_handler.send({
            "type": TURN_UPDATE,
            "status": "OK",
            "room_id": handler.room_id,
            "payload": {
                "current_turn_session_id": room.current_turn
            }
        })


def handle_forfeit(handler):
    if not handler.room_id:
        handler.send_error("You are not in a room")
        return

    room = handler.matchmaking.room_manager.get_room(handler.room_id)

    if not room:
        handler.send_error("Room not found")
        return

    opponent = room.get_opponent(handler.session_id)

    if opponent is None:
        handler.send_error("Opponent not found")
        return

    winner_player = opponent
    loser_player = get_current_player_data(handler, room)

    room.status = "FINISHED"
    room.winner = winner_player["session_id"]

    record_match_result(
        winner_username=winner_player["username"],
        loser_username=loser_player["username"]
    )

    add_forfeit_event(
        room_id=handler.room_id,
        loser=loser_player["username"],
        winner=winner_player["username"]
    )

    finish_replay(
        room_id=handler.room_id,
        winner=winner_player["username"]
    )

    for player in room.players:
        player_handler = player["handler"]

        player_handler.send({
            "type": GAME_OVER,
            "status": "OK",
            "room_id": handler.room_id,
            "payload": {
                "winner_session_id": winner_player["session_id"],
                "message": f"{loser_player['username']} forfeited"
            }
        })

    if len(room.players) >= 2:
        player_1 = room.players[0]
        player_2 = room.players[1]

        for spectator in room.spectators:
            spectator_handler = spectator["handler"]

            spectator_handler.send({
                "type": SPECTATOR_UPDATE,
                "status": "OK",
                "room_id": handler.room_id,
                "payload": {
                    "message": f"{loser_player['username']} forfeited",
                    "player_1": player_1["username"],
                    "player_2": player_2["username"],
                    "player_1_board": room.get_spectator_board(player_1["session_id"]),
                    "player_2_board": room.get_spectator_board(player_2["session_id"]),
                    "player_1_ships": room.get_ship_layout(player_1["session_id"]),
                    "player_2_ships": room.get_ship_layout(player_2["session_id"]),
                    "spectator_count": len(room.spectators),
                    "current_turn_session_id": room.current_turn,
                    "winner_session_id": winner_player["session_id"]
                }
            })

    handler.logger.info(
        f"Game over by forfeit in room {handler.room_id}. "
        f"Winner: {winner_player['username']}"
    )
