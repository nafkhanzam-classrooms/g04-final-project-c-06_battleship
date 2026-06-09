from shared.constants import BOARD_SIZE, SHIPS, CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS


def center_x(object_width):
    return (WIDTH - object_width) // 2


def get_latency_display():
    if not latency_auto_enabled or latency_ms is None:
        return "Click P"

    return f"{latency_ms} ms"


def get_filtered_rooms():
    query = room_search_input.text.strip().lower()

    if not query:
        return available_rooms

    result = []
    for room in available_rooms:
        room_name = room.get("room_name", "").lower()
        room_id_value = room.get("room_id", "").lower()

        if query in room_name or query in room_id_value:
            result.append(room)

    return result


def request_room_list():
    global room_browser_status

    room_browser_status = "Loading rooms..."

    client.send({
        "type": GET_ROOM_LIST,
        "session_id": session_id,
        "payload": {}
    })


def format_room_status(room):
    status = room.get("status", "UNKNOWN")

    if status in ["WAITING_OPPONENT", "WAITING_PLACEMENT"]:
        return "WAITING"

    if status == "IN_GAME":
        return "PLAY"

    if status == "FINISHED":
        return "FINISHED"

    return status


def format_room_lock(room):
    return "LOCK" if room.get("has_password") else "OPEN"


def filter_rooms():
    keyword = room_search_input.text.strip().lower()

    if not keyword:
        return available_rooms

    result = []

    for room in available_rooms:
        room_name = room.get("room_name", "").lower()
        room_id_value = room.get("room_id", "").lower()

        if keyword in room_name or keyword in room_id_value:
            result.append(room)

    return result


def reset_game_state():
    global placed_ships, current_ship_index, orientation, placement_confirm_open
    global game_paused, game_pause_screen
    global local_board, enemy_board
    global ships_submitted, current_turn_session_id, winner_session_id

    placed_ships = []
    current_ship_index = 0
    orientation = "H"
    placement_confirm_open = False
    game_paused = False
    game_pause_screen = "MENU"

    local_board = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    enemy_board = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    ships_submitted = False
    current_turn_session_id = None
    winner_session_id = None


def validate_auth_input():
    entered_username = username_input.text.strip()
    entered_password = password_input.text.strip()

    if not entered_username:
        return False, "Username wajib diisi"

    if not entered_password:
        return False, "Password wajib diisi"

    if len(entered_username) < 3:
        return False, "Username minimal 3 karakter"

    if len(entered_password) < 4:
        return False, "Password minimal 4 karakter"

    return True, ""


def send_login_from_auth():
    global status_text

    valid, message = validate_auth_input()

    if not valid:
        status_text = message
        return

    status_text = "Logging in..."

    client.send({
        "type": LOGIN,
        "payload": {
            "username": username_input.text.strip(),
            "password": password_input.text.strip()
        }
    })


def send_register_from_auth():
    global status_text

    valid, message = validate_auth_input()

    if not valid:
        status_text = message
        return

    status_text = "Registering..."

    client.send({
        "type": REGISTER,
        "payload": {
            "username": username_input.text.strip(),
            "password": password_input.text.strip()
        }
    })


def leave_current_room():
    global room_id, opponent_username, player_index
    global status_text, screen_state

    if room_id and session_id:
        client.send({
            "type": LEAVE_ROOM,
            "session_id": session_id,
            "room_id": room_id,
            "payload": {}
        })

    room_id = None
    opponent_username = None
    player_index = None
    status_text = "Left room"
    screen_state = "MAIN_MENU"


def get_ship_dimensions(ship, orient):
    width = ship.get("width", ship.get("size", 1))
    height = ship.get("height", 1)

    if orient == "V":
        width, height = height, width

    return width, height


def get_ship_cells(start_x, start_y, ship, orient):
    cells = []
    width, height = get_ship_dimensions(ship, orient)

    for y_offset in range(height):
        for x_offset in range(width):
            cells.append({
                "x": start_x + x_offset,
                "y": start_y + y_offset
            })

    return cells


def can_place_ship(cells):
    for cell in cells:
        x = cell["x"]
        y = cell["y"]

        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return False

        if local_board[y][x] == CELL_SHIP:
            return False

    return True


def place_ship_at_grid(grid_x, grid_y):
    global current_ship_index, status_text, placement_confirm_open

    if placement_confirm_open:
        return

    if current_ship_index >= len(SHIPS):
        placement_confirm_open = True
        status_text = "All ships placed. Confirm your placement."
        return

    ship = SHIPS[current_ship_index]
    cells = get_ship_cells(grid_x, grid_y, ship, orientation)

    if not can_place_ship(cells):
        status_text = "Invalid placement"
        return

    for cell in cells:
        local_board[cell["y"]][cell["x"]] = CELL_SHIP

    placed_ships.append({
        "name": ship["name"],
        "width": ship.get("width", ship.get("size", 1)),
        "height": ship.get("height", 1),
        "orientation": orientation,
        "cells": cells
    })

    current_ship_index += 1

    if current_ship_index >= len(SHIPS):
        placement_confirm_open = True
        status_text = "All ships placed. Confirm your placement."
    else:
        status_text = f"Place ship: {SHIPS[current_ship_index]['name']}"


def get_ship_bounds(cells):
    min_x = min(cell["x"] for cell in cells)
    max_x = max(cell["x"] for cell in cells)
    min_y = min(cell["y"] for cell in cells)
    max_y = max(cell["y"] for cell in cells)
    return min_x, min_y, max_x, max_y


def undo_last_ship():
    global current_ship_index, status_text, placement_confirm_open

    if not placed_ships:
        status_text = "No ship to undo"
        placement_confirm_open = False
        return

    last_ship = placed_ships.pop()

    for cell in last_ship["cells"]:
        x = cell["x"]
        y = cell["y"]

        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            local_board[y][x] = CELL_EMPTY

    current_ship_index = max(0, current_ship_index - 1)
    placement_confirm_open = False

    if current_ship_index < len(SHIPS):
        status_text = f"Place ship: {SHIPS[current_ship_index]['name']}"
    else:
        status_text = "All ships placed. Confirm your placement."


def submit_placed_ships():
    global placement_confirm_open, status_text

    if current_ship_index < len(SHIPS):
        status_text = "Place all ships first"
        return

    placement_confirm_open = False
    status_text = "Submitting ships..."

    client.send({
        "type": PLACE_SHIPS,
        "session_id": session_id,
        "room_id": room_id,
        "payload": {
            "ships": placed_ships
        }
    })


def get_board_stats(board):
    hits = 0
    misses = 0

    for row in board:
        for cell in row:
            if cell == CELL_HIT:
                hits += 1
            elif cell == CELL_MISS:
                misses += 1

    return hits, misses


def build_board_from_ships(ships):
    board = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    for ship in ships:
        for cell in ship.get("cells", []):
            x = cell.get("x")
            y = cell.get("y")

            if isinstance(x, int) and isinstance(y, int) and 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                board[y][x] = CELL_SHIP

    return board


def apply_replay_events(board_1, board_2, replay, step_index):
    events = replay.get("events", [])
    player_1 = replay.get("player_1")
    player_2 = replay.get("player_2")

    for event in events[:step_index]:
        shooter = event.get("shooter")
        x = event.get("x")
        y = event.get("y")
        result = event.get("result")

        if not isinstance(x, int) or not isinstance(y, int):
            continue

        target_board = board_2 if shooter == player_1 else board_1

        if result == "HIT":
            target_board[y][x] = CELL_HIT
        elif result == "MISS":
            target_board[y][x] = CELL_MISS


def build_replay_board(replay, side, step_index):
    if not replay:
        return [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    ships_1 = replay.get("player_1_ships", [])
    ships_2 = replay.get("player_2_ships", [])

    board_1 = build_board_from_ships(ships_1)
    board_2 = build_board_from_ships(ships_2)

    apply_replay_events(board_1, board_2, replay, step_index)

    return board_1 if side == 1 else board_2


def open_replay_for_current_room(source_state):
    global replay_source_state, replay_step_index

    replay_source_state = source_state
    replay_step_index = 0

    client.send({
        "type": GET_REPLAY_DETAIL,
        "session_id": session_id,
        "payload": {
            "room_id": room_id
        }
    })


def get_my_leaderboard_stat():
    for player in leaderboard_data:
        if player.get("username") == username:
            return player

    return {
        "username": username,
        "total_match": 0,
        "win": 0,
        "lose": 0,
        "hit_count": 0,
        "miss_count": 0,
        "win_rate": 0
    }
