from server.replay_service import create_replay
from shared.message_type import ROOM_WAITING_CREATED, MATCH_FOUND


def handle_matchmake(handler):
    if not handler.session_id:
        handler.send_error("You must login first")
        return

    player = {
        "username": handler.username,
        "session_id": handler.session_id,
        "handler": handler
    }

    room, is_matched = handler.matchmaking.join_queue(player)

    handler.room_id = room.room_id

    if not is_matched:
        handler.send({
            "type": ROOM_WAITING_CREATED,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "message": "Waiting for another player...",
                "room_id": room.room_id,
                "host_username": handler.username
            }
        })

        handler.logger.info(
            f"Waiting room created: {room.room_id} | host={handler.username}"
        )
        return

    room_id = room.room_id
    players = room.players

    for index, player_data in enumerate(players):
        player_handler = player_data["handler"]
        player_handler.room_id = room_id

        opponent = players[1 - index]

        player_handler.send({
            "type": MATCH_FOUND,
            "status": "OK",
            "room_id": room_id,
            "payload": {
                "player_index": index + 1,
                "your_username": player_data["username"],
                "opponent_username": opponent["username"],
                "message": "Match found"
            }
        })

    create_replay(
        room_id=room_id,
        player_1=players[0]["username"],
        player_2=players[1]["username"]
    )

    handler.logger.info(
        f"Room matched: {room_id} | "
        f"{players[0]['username']} vs {players[1]['username']}"
    )
