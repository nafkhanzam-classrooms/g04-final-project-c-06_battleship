import json
import os
from datetime import datetime


REPLAY_DIR = "data/replays"


def ensure_replay_dir():
    os.makedirs(REPLAY_DIR, exist_ok=True)


def create_replay(room_id, player_1, player_2):
    ensure_replay_dir()

    replay = {
        "room_id": room_id,
        "player_1": player_1,
        "player_2": player_2,
        "started_at": datetime.now().isoformat(),
        "finished_at": None,
        "winner": None,
        "player_1_ships": [],
        "player_2_ships": [],
        "events": []
    }

    save_replay(room_id, replay)
    return replay


def save_replay(room_id, replay):
    ensure_replay_dir()

    path = os.path.join(REPLAY_DIR, f"{room_id}.json")

    with open(path, "w", encoding="utf-8") as file:
        json.dump(replay, file, indent=4)



def save_ship_layouts(room_id, player_1_ships, player_2_ships):
    replay = get_replay(room_id)

    if replay is None:
        return

    replay["player_1_ships"] = player_1_ships
    replay["player_2_ships"] = player_2_ships

    save_replay(room_id, replay)


def add_fire_event(room_id, shooter, x, y, result, turn_number):
    replay = get_replay(room_id)

    if replay is None:
        return

    replay["events"].append({
        "turn": turn_number,
        "shooter": shooter,
        "action": "FIRE",
        "x": x,
        "y": y,
        "result": result,
        "timestamp": datetime.now().isoformat()
    })

    save_replay(room_id, replay)



def add_forfeit_event(room_id, loser, winner):
    replay = get_replay(room_id)

    if replay is None:
        return

    next_turn = len(replay.get("events", [])) + 1

    replay["events"].append({
        "turn": next_turn,
        "shooter": loser,
        "action": "FORFEIT",
        "x": None,
        "y": None,
        "result": "FORFEIT",
        "winner": winner,
        "timestamp": datetime.now().isoformat()
    })

    save_replay(room_id, replay)


def finish_replay(room_id, winner):
    replay = get_replay(room_id)

    if replay is None:
        return

    replay["winner"] = winner
    replay["finished_at"] = datetime.now().isoformat()

    save_replay(room_id, replay)


def get_replay(room_id):
    path = os.path.join(REPLAY_DIR, f"{room_id}.json")

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_replay_list():
    ensure_replay_dir()

    replay_list = []

    for filename in os.listdir(REPLAY_DIR):
        if not filename.endswith(".json"):
            continue

        room_id = filename.replace(".json", "")
        replay = get_replay(room_id)

        if replay:
            replay_list.append({
                "room_id": replay["room_id"],
                "player_1": replay["player_1"],
                "player_2": replay["player_2"],
                "winner": replay["winner"],
                "started_at": replay["started_at"],
                "finished_at": replay["finished_at"],
                "total_events": len(replay["events"])
            })

    replay_list.sort(key=lambda item: item["started_at"], reverse=True)
    return replay_list