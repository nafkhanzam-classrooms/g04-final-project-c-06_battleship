from server.response_builder import ok, failed, room_payload
from server.replay_service import create_replay
from shared.message_type import (
    CREATE_ROOM_SUCCESS,
    CREATE_ROOM_FAILED,
    ROOM_LIST_DATA,
    JOIN_ROOM_SUCCESS,
    JOIN_ROOM_FAILED,
    ROOM_UPDATED,
    MATCH_FOUND,
    SPECTATOR_JOINED
)


def notify_room_updated(handler, room):
    if not room:
        return

    for player in room.players:
        player["handler"].send({
            "type": ROOM_UPDATED,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "room": room.get_public_info()
            }
        })

    for spectator in room.spectators:
        spectator["handler"].send({
            "type": ROOM_UPDATED,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "room": room.get_public_info()
            }
        })


def notify_match_found(handler, room):
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


def build_spectator_payload(room, message="Joined as spectator"):
    player_1 = room.players[0]
    player_2 = room.players[1] if len(room.players) > 1 else None

    return {
        "message": message,
        "player_1": player_1["username"],
        "player_2": player_2["username"] if player_2 else "Waiting",
        "player_1_session_id": player_1["session_id"],
        "player_2_session_id": player_2["session_id"] if player_2 else None,
        "player_1_board": (
            room.get_spectator_board(player_1["session_id"])
            if room.status == "IN_GAME"
            else room.create_empty_board()
        ),
        "player_2_board": (
            room.get_spectator_board(player_2["session_id"])
            if player_2 and room.status == "IN_GAME"
            else room.create_empty_board()
        ),
        "player_1_ships": (
            room.get_ship_layout(player_1["session_id"])
            if room.status == "IN_GAME"
            else []
        ),
        "player_2_ships": (
            room.get_ship_layout(player_2["session_id"])
            if player_2 and room.status == "IN_GAME"
            else []
        ),
        "room_status": room.status,
        "spectator_count": len(room.spectators),
        "current_turn_session_id": room.current_turn
    }


def handle_create_room(handler, message):
    if not handler.session_id:
        handler.send_error("You must login first")
        return

    payload = message.get("payload", {})
    room_name = payload.get("room_name", "").strip()
    password = payload.get("password", "")

    if not room_name:
        handler.send(failed(CREATE_ROOM_FAILED, "Room name wajib diisi"))
        return

    player = {
        "username": handler.username,
        "session_id": handler.session_id,
        "handler": handler
    }

    room = handler.matchmaking.room_manager.create_manual_room(
        player_1=player,
        room_name=room_name,
        password=password
    )

    handler.room_id = room.room_id

    handler.send(room_payload(
        CREATE_ROOM_SUCCESS,
        room,
        message="Room created"
    ))

    handler.logger.info(
        f"Manual room created: {room.room_id} | "
        f"name={room.room_name} | host={handler.username}"
    )


def handle_get_room_list(handler):
    rooms = handler.matchmaking.room_manager.get_room_list()

    handler.send(ok(
        ROOM_LIST_DATA,
        payload={
            "rooms": rooms
        }
    ))


def handle_join_room(handler, message):
    if not handler.session_id:
        handler.send_error("You must login first")
        return

    payload = message.get("payload", {})
    room_id = payload.get("room_id")
    password = payload.get("password", "")
    mode = payload.get("mode", "PLAYER")

    if not room_id:
        handler.send(failed(JOIN_ROOM_FAILED, "Room ID is required"))
        return

    user_data = {
        "username": handler.username,
        "session_id": handler.session_id,
        "handler": handler
    }

    if mode == "SPECTATOR":
        success, info, room = handler.matchmaking.room_manager.join_room_as_spectator(
            room_id=room_id,
            spectator=user_data,
            password=password
        )

        if not success:
            handler.send(failed(JOIN_ROOM_FAILED, info))
            return

        handler.room_id = room.room_id

        handler.send(ok(
            SPECTATOR_JOINED,
            room_id=room.room_id,
            payload=build_spectator_payload(room)
        ))

        handler.logger.info(
            f"{handler.username} joined room {room_id} as spectator"
        )

        notify_room_updated(handler, room)
        return

    success, info, room = handler.matchmaking.room_manager.join_room_as_player(
        room_id=room_id,
        player=user_data,
        password=password
    )

    if not success:
        handler.send(failed(JOIN_ROOM_FAILED, info))
        return

    handler.room_id = room.room_id

    if len(room.players) == 2:
        notify_match_found(handler, room)
    else:
        handler.send(room_payload(
            JOIN_ROOM_SUCCESS,
            room,
            message=info
        ))


def handle_leave_room(handler):
    if not handler.room_id:
        return

    old_room_id = handler.room_id

    room = handler.matchmaking.room_manager.remove_user_from_room(
        old_room_id,
        handler.session_id
    )

    handler.room_id = None

    if room:
        notify_room_updated(handler, room)

    handler.logger.info(f"{handler.username} left room {old_room_id}")