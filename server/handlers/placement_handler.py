from server.replay_service import save_ship_layouts
from shared.message_type import (
    PLACEMENT_START,
    PLACE_SHIPS_SUCCESS,
    PLACE_SHIPS_ERROR,
    WAITING_OPPONENT_READY,
    GAME_START,
    SPECTATOR_UPDATE
)


def send_placement_start_to_room(handler, room):
    for index, player in enumerate(room.players):
        player_handler = player["handler"]
        opponent = room.players[1 - index] if len(room.players) > 1 else None

        player_handler.send({
            "type": PLACEMENT_START,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "room": room.get_public_info(),
                "player_index": index + 1,
                "opponent_username": opponent["username"] if opponent else None,
                "message": "Placement started"
            }
        })

    for spectator in room.spectators:
        spectator_handler = spectator["handler"]

        spectator_handler.send({
            "type": PLACEMENT_START,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "room": room.get_public_info(),
                "spectator": True,
                "spectator_count": len(room.spectators),
                "message": "Players are placing ships"
            }
        })


def handle_start_placement(handler):
    if not handler.room_id:
        handler.send_error("You are not in a room")
        return

    room = handler.matchmaking.room_manager.get_room(handler.room_id)

    if not room:
        handler.send_error("Room not found")
        return

    if len(room.players) < 2:
        handler.send_error("Need 2 players to start")
        return

    room.status = "WAITING_PLACEMENT"
    send_placement_start_to_room(handler, room)

    handler.logger.info(f"Placement started in room {handler.room_id}")


def handle_place_ships(handler, message):
    if not handler.room_id:
        handler.send_error("You are not in a room")
        return

    room = handler.matchmaking.room_manager.get_room(handler.room_id)

    if not room:
        handler.send_error("Room not found")
        return

    ships = message.get("payload", {}).get("ships", [])

    success, info = room.place_ships(handler.session_id, ships)

    if not success:
        handler.send({
            "type": PLACE_SHIPS_ERROR,
            "status": "ERROR",
            "room_id": handler.room_id,
            "payload": {
                "message": info
            }
        })
        return

    handler.logger.info(f"{handler.username} placed ships in room {handler.room_id}")

    handler.send({
        "type": PLACE_SHIPS_SUCCESS,
        "status": "OK",
        "room_id": handler.room_id,
        "payload": {
            "message": info
        }
    })


def handle_ready(handler, message):
    if not handler.room_id:
        handler.send_error("You are not in a room")
        return

    room = handler.matchmaking.room_manager.get_room(handler.room_id)

    if not room:
        handler.send_error("Room not found")
        return

    game_started = room.set_ready(handler.session_id)

    if not game_started:
        handler.send({
            "type": WAITING_OPPONENT_READY,
            "status": "OK",
            "room_id": handler.room_id,
            "payload": {
                "message": "Waiting for opponent to be ready"
            }
        })
        return

    for player in room.players:
        player_handler = player["handler"]

        player_handler.send({
            "type": GAME_START,
            "status": "OK",
            "room_id": handler.room_id,
            "payload": {
                "first_turn_session_id": room.current_turn,
                "message": "Game started"
            }
        })

    if len(room.players) >= 2:
        player_1 = room.players[0]
        player_2 = room.players[1]

        save_ship_layouts(
            room_id=handler.room_id,
            player_1_ships=room.get_ship_layout(player_1["session_id"]),
            player_2_ships=room.get_ship_layout(player_2["session_id"])
        )

        for spectator in room.spectators:
            spectator_handler = spectator["handler"]

            spectator_handler.send({
                "type": SPECTATOR_UPDATE,
                "status": "OK",
                "room_id": handler.room_id,
                "payload": {
                    "message": "Game started",
                    "player_1": player_1["username"],
                    "player_2": player_2["username"],
                    "player_1_board": room.get_spectator_board(player_1["session_id"]),
                    "player_2_board": room.get_spectator_board(player_2["session_id"]),
                    "player_1_ships": room.get_ship_layout(player_1["session_id"]),
                    "player_2_ships": room.get_ship_layout(player_2["session_id"]),
                    "spectator_count": len(room.spectators),
                    "current_turn_session_id": room.current_turn,
                    "winner_session_id": None
                }
            })

    handler.logger.info(f"Game started in room {handler.room_id}")
