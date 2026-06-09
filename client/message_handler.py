from shared.constants import SHIPS, BOARD_SIZE, CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS
from shared.message_type import *


def handle_server_message(message):
    global username, session_id, room_id, opponent_username, player_index
    global latency_ms, status_text, screen_state, ships_submitted
    global latency_auto_enabled, last_ping_time, game_paused, game_pause_screen
    global current_turn_session_id, winner_session_id
    global is_spectator, spectator_player_1, spectator_player_2
    global spectator_board_1, spectator_board_2
    global spectator_ships_1, spectator_ships_2, spectator_paused, spectator_pause_screen
    global leaderboard_data
    global leaderboard_mode, leaderboard_scroll_offset
    global replay_list, selected_replay
    global available_rooms, selected_room, selected_room_index, room_browser_status
    global current_spectator_count, spectator_room_status
    global current_spectator_count
    global username, session_id, room_id, opponent_username, player_index

    if message["type"] == LOGIN_SUCCESS:
        session_id = message["session_id"]
        username = message["payload"]["username"]
        status_text = "Login success"
        screen_state = "MAIN_MENU"

    elif message["type"] == LOGIN_FAILED:
        status_text = message["payload"]["message"]
        screen_state = "AUTH"

    elif message["type"] == REGISTER_SUCCESS:
        status_text = "Register berhasil. Silakan login."
        screen_state = "AUTH"

    elif message["type"] == REGISTER_FAILED:
        status_text = message["payload"]["message"]
        screen_state = "AUTH"

    elif message["type"] == ROOM_WAITING_CREATED:
        room_id = message["room_id"]
        opponent_username = None
        player_index = 1
        status_text = "Waiting for another player..."
        screen_state = "ROOM_WAITING"

    elif message["type"] == CREATE_ROOM_SUCCESS:
        room = message["payload"]["room"]
        current_spectator_count = room.get("spectator_count", 0)
        room_id = message["room_id"]
        opponent_username = None
        player_index = 1
        create_room_name_input.text = ""
        create_room_password_input.text = ""
        status_text = "Room created. Waiting for opponent."
        screen_state = "ROOM_WAITING"

    elif message["type"] == CREATE_ROOM_FAILED:
        status_text = message["payload"]["message"]
        screen_state = "CREATE_ROOM"

    elif message["type"] == ROOM_LIST_DATA:
        available_rooms = message["payload"].get("rooms", [])
        selected_room = None
        selected_room_index = None
        room_browser_status = f"Loaded {len(available_rooms)} room(s)"
        screen_state = "ROOM_BROWSER"

    elif message["type"] == JOIN_ROOM_SUCCESS:
        room_id = message["room_id"]
        room = message["payload"].get("room", {})
        current_spectator_count = room.get("spectator_count", 0)
        players = room.get("players", [])
        opponent_username = None
        player_index = len(players)
        status_text = message["payload"].get("message", "Joined room")
        screen_state = "ROOM_WAITING"

    elif message["type"] == JOIN_ROOM_FAILED:
        status_text = message["payload"]["message"]
        room_browser_status = status_text
        selected_room_index = None
        popup_password_input.text = ""
        screen_state = "ROOM_BROWSER"

    elif message["type"] == WAITING_FOR_PLAYER:
        status_text = "Waiting for another player..."
        screen_state = "ROOM_WAITING"

    elif message["type"] == MATCH_FOUND:
        room_id = message["room_id"]
        opponent_username = message["payload"]["opponent_username"]
        player_index = message["payload"]["player_index"]
        status_text = "Opponent found. Press Start / Continue."
        screen_state = "ROOM_WAITING"

    elif message["type"] == ROOM_UPDATED:
        room = message["payload"]["room"]
        current_spectator_count = room.get("spectator_count", current_spectator_count)
        players = room.get("players", [])

        if len(players) == 1:
            # Kalau sedang battle dan update ini cuma karena spectator keluar/masuk,
            # jangan tendang player ke room waiting. Player cuma perlu update spectator count.
            if screen_state == "GAME":
                status_text = f"Spectators: {current_spectator_count}"
            else:
                opponent_username = None
                player_index = 1
                status_text = "Opponent left. Waiting for another player..."
                screen_state = "ROOM_WAITING"

        elif len(players) == 2:
            if players[0] == username:
                opponent_username = players[1]
                player_index = 1
            elif players[1] == username:
                opponent_username = players[0]
                player_index = 2

            # Penting: kalau game sedang berjalan, ROOM_UPDATED dari spectator join/leave
            # tidak boleh mengubah screen_state player.
            if screen_state == "GAME":
                status_text = f"Spectators: {current_spectator_count}"
            elif screen_state in ["SPECTATOR", "SPECTATOR_WAITING"]:
                status_text = f"Spectators: {current_spectator_count}"
            else:
                status_text = "Room updated"
                screen_state = "ROOM_WAITING"

    elif message["type"] == PLACEMENT_START:
        room = message["payload"].get("room", {})
        current_spectator_count = room.get("spectator_count", current_spectator_count)

        if message["payload"].get("spectator"):
            spectator_room_status = "WAITING_PLACEMENT"
            status_text = "Players are placing ships..."
            screen_state = "SPECTATOR_WAITING"
        else:
            player_index = message["payload"].get("player_index", player_index)
            opponent_username = message["payload"].get("opponent_username", opponent_username)
            reset_game_state()
            status_text = f"Place ship: {SHIPS[current_ship_index]['name']}"
            screen_state = "PLACEMENT"

    elif message["type"] == REMATCH_WAITING:
        room = message["payload"].get("room", {})
        room_id = message.get("room_id", room_id)
        opponent_username = None
        player_index = 1
        current_spectator_count = room.get("spectator_count", current_spectator_count)
        reset_game_state()
        status_text = "Waiting for rematch opponent..."
        screen_state = "ROOM_WAITING"

    elif message["type"] == PLACE_SHIPS_SUCCESS:
        ships_submitted = True
        placement_confirm_open = False
        status_text = "Ships submitted. Press ENTER again to ready."

    elif message["type"] == PLACE_SHIPS_ERROR:
        placement_confirm_open = False
        status_text = "Placement error: " + message["payload"]["message"]

    elif message["type"] == WAITING_OPPONENT_READY:
        status_text = "Waiting opponent ready..."

    elif message["type"] == GAME_START:
        current_turn_session_id = message["payload"]["first_turn_session_id"]

        if current_turn_session_id == session_id:
            status_text = "Game started. Your turn."
        else:
            status_text = "Game started. Opponent turn."

        screen_state = "GAME"

    elif message["type"] == SPECTATOR_JOINED:
        is_spectator = True
        room_id = message["room_id"]

        spectator_player_1 = message["payload"]["player_1"]
        spectator_player_2 = message["payload"]["player_2"]
        spectator_board_1 = message["payload"]["player_1_board"]
        spectator_board_2 = message["payload"]["player_2_board"]
        spectator_ships_1 = message["payload"].get("player_1_ships", [])
        spectator_ships_2 = message["payload"].get("player_2_ships", [])
        spectator_room_status = message["payload"].get("room_status", "WAITING_OPPONENT")
        current_spectator_count = message["payload"].get("spectator_count", current_spectator_count)

        if spectator_room_status == "IN_GAME":
            status_text = "Watching battle"
            screen_state = "SPECTATOR"
        elif spectator_room_status == "WAITING_PLACEMENT":
            status_text = "Players are placing ships..."
            screen_state = "SPECTATOR_WAITING"
        else:
            status_text = "Waiting for game to start"
            screen_state = "SPECTATOR_WAITING"

    elif message["type"] == SPECTATOR_UPDATE:
        spectator_player_1 = message["payload"].get("player_1", spectator_player_1)
        spectator_player_2 = message["payload"].get("player_2", spectator_player_2)
        spectator_board_1 = message["payload"]["player_1_board"]
        spectator_board_2 = message["payload"]["player_2_board"]
        spectator_ships_1 = message["payload"].get("player_1_ships", spectator_ships_1)
        spectator_ships_2 = message["payload"].get("player_2_ships", spectator_ships_2)
        current_spectator_count = message["payload"].get("spectator_count", current_spectator_count)

        result = message["payload"].get("result")
        if result:
            status_text = f"Spectator update: {result}"
        else:
            status_text = message["payload"].get("message", "Watching battle")

        if message["payload"].get("winner_session_id"):
            status_text = message["payload"].get("message", "Game over")
            open_replay_for_current_room("SPECTATOR_RESULT")
        else:
            spectator_room_status = "IN_GAME"
            screen_state = "SPECTATOR"

    elif message["type"] == FIRE_RESULT:
        payload = message["payload"]
        x = payload["x"]
        y = payload["y"]

        if payload["result"] == "HIT":
            enemy_board[y][x] = CELL_HIT
            status_text = "Hit!"
        else:
            enemy_board[y][x] = CELL_MISS
            status_text = "Miss!"

        current_turn_session_id = payload["next_turn_session_id"]

    elif message["type"] == OPPONENT_FIRE_RESULT:
        payload = message["payload"]
        x = payload["x"]
        y = payload["y"]

        if payload["result"] == "HIT":
            local_board[y][x] = CELL_HIT
            status_text = "Your ship was hit!"
        else:
            local_board[y][x] = CELL_MISS
            status_text = "Opponent missed."

        current_turn_session_id = payload["next_turn_session_id"]

    elif message["type"] == TURN_UPDATE:
        current_turn_session_id = message["payload"]["current_turn_session_id"]

        if current_turn_session_id == session_id:
            status_text = "Your turn."
        else:
            status_text = "Opponent turn."

    elif message["type"] == REPLAY_LIST_DATA:
        replay_list = message["payload"]["replays"]
        screen_state = "REPLAY_LIST"

    elif message["type"] == REPLAY_DETAIL_DATA:
        selected_replay = message["payload"]["replay"]

        if replay_source_state == "GAME_OVER":
            replay_step_index = 0
            screen_state = "REPLAY_VIEWER"
        elif replay_source_state == "SPECTATOR_RESULT":
            screen_state = "SPECTATOR_RESULT"
        elif replay_source_state == "SPECTATOR_REPLAY":
            replay_step_index = 0
            screen_state = "REPLAY_VIEWER"
        else:
            screen_state = "REPLAY_DETAIL"

    elif message["type"] == GAME_OVER:
        winner_session_id = message["payload"]["winner_session_id"]
        game_paused = False
        game_pause_screen = "MENU"
        status_text = message["payload"].get("message", "Game over")
        screen_state = "GAME_OVER"

    elif message["type"] == LEADERBOARD_DATA:
        leaderboard_data = message["payload"]["leaderboard"]
        screen_state = "LEADERBOARD"

    elif message["type"] == PONG:
        sent_at = message["payload"].get("sent_at")
        if sent_at:
            latency_ms = round(pygame.time.get_ticks() - sent_at, 1)

    elif message["type"] == ERROR:
        status_text = "Error: " + message["payload"]["message"]
