from server.response_builder import ok
from server.ranking_service import get_leaderboard
from shared.message_type import LEADERBOARD_DATA


def handle_get_leaderboard(handler):
    leaderboard = get_leaderboard()

    handler.send(ok(
        LEADERBOARD_DATA,
        payload={
            "leaderboard": leaderboard
        }
    ))
