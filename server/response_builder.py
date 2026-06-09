def ok(message_type, payload=None, room_id=None, session_id=None):
    response = {
        "type": message_type,
        "status": "OK",
        "payload": payload or {}
    }

    if room_id is not None:
        response["room_id"] = room_id

    if session_id is not None:
        response["session_id"] = session_id

    return response


def failed(message_type, message, room_id=None):
    response = {
        "type": message_type,
        "status": "ERROR",
        "payload": {
            "message": message
        }
    }

    if room_id is not None:
        response["room_id"] = room_id

    return response


def error(message):
    return {
        "type": "ERROR",
        "status": "ERROR",
        "payload": {
            "message": message
        }
    }


def room_payload(message_type, room, message="", room_id=None):
    return ok(
        message_type,
        room_id=room_id or room.room_id,
        payload={
            "room": room.get_public_info(),
            "message": message
        }
    )
