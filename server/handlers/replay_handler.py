from server.response_builder import ok
from server.replay_service import get_replay_list, get_replay
from shared.message_type import REPLAY_LIST_DATA, REPLAY_DETAIL_DATA


def handle_get_replay_list(handler):
    handler.send(ok(
        REPLAY_LIST_DATA,
        payload={
            "replays": get_replay_list()
        }
    ))


def handle_get_replay_detail(handler, message):
    room_id = message.get("payload", {}).get("room_id")

    if not room_id:
        handler.send_error("Room ID is required")
        return

    replay = get_replay(room_id)

    if replay is None:
        handler.send_error("Replay not found")
        return

    handler.send(ok(
        REPLAY_DETAIL_DATA,
        payload={
            "replay": replay
        }
    ))
