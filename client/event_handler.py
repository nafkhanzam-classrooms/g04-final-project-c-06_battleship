import pygame


def run_loop():
    global screen, screen_state, status_text, running, latency_auto_enabled, last_ping_time, latency_ms, orientation, game_paused, game_pause_screen, fullscreen_enabled, sound_enabled, volume, room_id, opponent_username, player_index, selected_room_index, selected_room, room_browser_status, leaderboard_mode, leaderboard_scroll_offset, replay_step_index, secret_music_enabled, easter_popup_open, easter_pending_secret_state, spectator_paused, spectator_pause_screen, placement_confirm_open


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and screen_state == "TITLE":
                screen_state = "AUTH"
                status_text = "Please login or register"
                continue

            if screen_state == "AUTH":
                username_input.handle_event(event)
                password_input.handle_event(event)

                if login_button.is_clicked(event):
                    send_login_from_auth()

                elif register_button.is_clicked(event):
                    send_register_from_auth()

            if screen_state == "ROOM_BROWSER":
                room_search_input.handle_event(event)

                if selected_room_index is not None:
                    visible_rooms = filter_rooms()

                    if selected_room_index < len(visible_rooms):
                        selected_room_for_input = visible_rooms[selected_room_index]

                        if selected_room_for_input.get("has_password"):
                            popup_password_input.handle_event(event)

            if screen_state == "CREATE_ROOM":
                create_room_name_input.handle_event(event)
                create_room_password_input.handle_event(event)

            if event.type == pygame.MOUSEWHEEL and screen_state == "LEADERBOARD" and leaderboard_mode == "TOP":
                sorted_count = min(10, len(leaderboard_data))
                max_visible_rows = 6
                max_offset = max(0, sorted_count - max_visible_rows)

                if event.y < 0:
                    leaderboard_scroll_offset = min(max_offset, leaderboard_scroll_offset + 1)
                elif event.y > 0:
                    leaderboard_scroll_offset = max(0, leaderboard_scroll_offset - 1)

            if event.type == pygame.KEYDOWN:
                handle_easter_key(event)

                if event.key == pygame.K_ESCAPE:
                    if screen_state == "ROOM_WAITING":
                        leave_current_room()

                    elif screen_state in [
                        "LEADERBOARD",
                        "REPLAY_LIST",
                        "REPLAY_DETAIL",
                        "SETTINGS",
                        "ROOM_BROWSER",
                        "CREATE_ROOM",
                        "GAME_OVER"
                    ]:
                        screen_state = "MAIN_MENU"

                elif event.key == pygame.K_p and session_id and screen_state in ["GAME", "ROOM_WAITING", "SPECTATOR", "SPECTATOR_WAITING"]:
                    latency_auto_enabled = not latency_auto_enabled

                    if latency_auto_enabled:
                        last_ping_time = pygame.time.get_ticks()
                        status_text = "Auto latency check ON"

                        client.send({
                            "type": PING,
                            "session_id": session_id,
                            "payload": {
                                "sent_at": last_ping_time
                            }
                        })
                    else:
                        latency_ms = None
                        status_text = "Auto latency check OFF"

                elif screen_state == "PLACEMENT":
                    if event.key == pygame.K_r and not placement_confirm_open:
                        orientation = "V" if orientation == "H" else "H"

                    elif event.key == pygame.K_z and not ships_submitted:
                        undo_last_ship()

                    elif event.key == pygame.K_RETURN:
                        if placement_confirm_open:
                            submit_placed_ships()

                        elif current_ship_index >= len(SHIPS) and not ships_submitted:
                            placement_confirm_open = True
                            status_text = "All ships placed. Confirm your placement."

                        elif ships_submitted:
                            client.send({
                                "type": READY,
                                "session_id": session_id,
                                "room_id": room_id,
                                "payload": {}
                            })

            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_state == "MAIN_MENU":
                    if easter_popup_open:
                        if easter_next_button.is_clicked(event):
                            secret_music_enabled = easter_pending_secret_state
                            easter_popup_open = False
                            easter_pending_secret_state = None
                            force_music_refresh()

                    elif quick_play_button.is_clicked(event):
                        reset_game_state()
                        status_text = "Joining quick play..."
                        room_id = None
                        opponent_username = None

                        client.send({
                            "type": MATCHMAKE,
                            "session_id": session_id,
                            "payload": {}
                        })

                        screen_state = "ROOM_WAITING"

                    elif play_button.is_clicked(event):
                        request_room_list()
                        screen_state = "ROOM_BROWSER"

                    elif leaderboard_button.is_clicked(event):
                        leaderboard_mode = "TOP"
                        leaderboard_scroll_offset = 0

                        client.send({
                            "type": GET_LEADERBOARD,
                            "session_id": session_id,
                            "payload": {}
                        })

                    elif settings_button.is_clicked(event):
                        screen_state = "SETTINGS"

                    elif exit_button.is_clicked(event):
                        running = False

                elif screen_state == "ROOM_WAITING":
                    if room_start_button.is_clicked(event):
                        if opponent_username:
                            client.send({
                                "type": START_PLACEMENT,
                                "session_id": session_id,
                                "room_id": room_id,
                                "payload": {}
                            })
                            status_text = "Starting placement..."
                        else:
                            status_text = "Cannot start. Waiting for opponent."

                    elif room_spectate_button.is_clicked(event):
                        status_text = "Spectate switch placeholder"

                elif screen_state == "SETTINGS":
                    if settings_sound_button.is_clicked(event):
                        sound_enabled = not sound_enabled
                        apply_music_volume()

                    elif settings_volume_down_button.is_clicked(event):
                        volume = max(0, volume - 10)
                        apply_music_volume()

                    elif settings_volume_up_button.is_clicked(event):
                        volume = min(100, volume + 10)
                        apply_music_volume()

                    elif settings_fullscreen_button.is_clicked(event):
                        fullscreen_enabled = not fullscreen_enabled

                        if fullscreen_enabled:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))

                    elif settings_back_button.is_clicked(event):
                        screen_state = "MAIN_MENU"

                elif screen_state == "ROOM_BROWSER":
                    if selected_room_index is not None:
                        visible_rooms = filter_rooms()

                        if selected_room_index < len(visible_rooms):
                            selected_room = visible_rooms[selected_room_index]

                            password_value = ""
                            if selected_room.get("has_password"):
                                password_value = popup_password_input.text.strip()

                            if join_as_player_button.is_clicked(event):
                                client.send({
                                    "type": JOIN_ROOM,
                                    "session_id": session_id,
                                    "payload": {
                                        "room_id": selected_room["room_id"],
                                        "password": password_value,
                                        "mode": "PLAYER"
                                    }
                                })

                                room_browser_status = "Joining as player..."
                                selected_room_index = None
                                popup_password_input.text = ""

                            elif join_as_spectator_button.is_clicked(event):
                                client.send({
                                    "type": JOIN_ROOM,
                                    "session_id": session_id,
                                    "payload": {
                                        "room_id": selected_room["room_id"],
                                        "password": password_value,
                                        "mode": "SPECTATOR"
                                    }
                                })

                                room_browser_status = "Joining as spectator..."
                                selected_room_index = None
                                popup_password_input.text = ""

                            elif join_cancel_button.is_clicked(event):
                                selected_room_index = None
                                popup_password_input.text = ""

                        else:
                            selected_room_index = None
                            popup_password_input.text = ""

                    else:
                        for index, item in enumerate(join_room_buttons):
                            if item["button"].is_clicked(event):
                                selected_room_index = index
                                popup_password_input.text = ""
                                break

                        if refresh_room_button.is_clicked(event):
                            request_room_list()

                        elif create_room_button.is_clicked(event):
                            status_text = "Fill room name and optional password"
                            screen_state = "CREATE_ROOM"

                        elif room_back_button.is_clicked(event):
                            screen_state = "MAIN_MENU"

                elif screen_state == "CREATE_ROOM":
                    if create_room_submit_button.is_clicked(event):
                        room_name = create_room_name_input.text.strip()

                        if not room_name:
                            status_text = "Room name wajib diisi"
                        else:
                            client.send({
                                "type": CREATE_ROOM,
                                "session_id": session_id,
                                "payload": {
                                    "room_name": room_name,
                                    "password": create_room_password_input.text
                                }
                            })

                    elif create_room_cancel_button.is_clicked(event):
                        screen_state = "ROOM_BROWSER"

                elif screen_state == "PLACEMENT":
                    if placement_confirm_open:
                        if placement_confirm_yes_button.is_clicked(event):
                            submit_placed_ships()

                        elif placement_confirm_no_button.is_clicked(event):
                            placement_confirm_open = False
                            status_text = "Continue editing. Press Z to undo."

                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        grid_x = (mouse_x - PLACEMENT_BOARD_X) // CELL_SIZE
                        grid_y = (mouse_y - PLACEMENT_BOARD_Y) // CELL_SIZE

                        if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                            place_ship_at_grid(grid_x, grid_y)

                elif screen_state == "LEADERBOARD":
                    if leaderboard_back_button.is_clicked(event):
                        screen_state = "MAIN_MENU"

                    elif leaderboard_mode == "TOP" and leaderboard_my_stat_button.is_clicked(event):
                        leaderboard_mode = "MY_STAT"

                    elif leaderboard_mode == "MY_STAT" and leaderboard_top_button.is_clicked(event):
                        leaderboard_mode = "TOP"
                        leaderboard_scroll_offset = 0

                elif screen_state == "GAME_OVER":
                    if game_over_rematch_button.is_clicked(event):
                        client.send({
                            "type": REMATCH_REQUEST,
                            "session_id": session_id,
                            "room_id": room_id,
                            "payload": {}
                        })
                        status_text = "Requesting rematch..."

                    elif game_over_replay_button.is_clicked(event):
                        open_replay_for_current_room("GAME_OVER")

                    elif game_over_main_menu_button.is_clicked(event):
                        leave_current_room()

                elif screen_state == "SPECTATOR_RESULT":
                    if spectator_continue_button.is_clicked(event):
                        # Return to current room state. The next ROOM_UPDATED/SPECTATOR_UPDATE will adjust view.
                        if spectator_room_status == "IN_GAME":
                            screen_state = "SPECTATOR"
                        else:
                            screen_state = "SPECTATOR_WAITING"

                    elif spectator_result_replay_button.is_clicked(event):
                        open_replay_for_current_room("SPECTATOR_REPLAY")

                    elif spectator_result_main_menu_button.is_clicked(event):
                        leave_current_room()

                elif screen_state == "REPLAY_VIEWER":
                    total_events = len(selected_replay.get("events", [])) if selected_replay else 0

                    if replay_prev_button.is_clicked(event):
                        replay_step_index = max(0, replay_step_index - 1)

                    elif replay_next_button.is_clicked(event):
                        replay_step_index = min(total_events, replay_step_index + 1)

                    elif replay_exit_button.is_clicked(event):
                        if replay_source_state == "GAME_OVER":
                            screen_state = "GAME_OVER"
                        elif replay_source_state in ["SPECTATOR_REPLAY", "SPECTATOR_RESULT"]:
                            screen_state = "SPECTATOR_RESULT"
                        else:
                            screen_state = "MAIN_MENU"

                elif screen_state == "GAME":
                    if game_paused:
                        if game_pause_screen == "SETTINGS":
                            if settings_sound_button.is_clicked(event):
                                sound_enabled = not sound_enabled
                                apply_music_volume()

                            elif settings_volume_down_button.is_clicked(event):
                                volume = max(0, volume - 10)
                                apply_music_volume()

                            elif settings_volume_up_button.is_clicked(event):
                                volume = min(100, volume + 10)
                                apply_music_volume()

                            elif settings_fullscreen_button.is_clicked(event):
                                fullscreen_enabled = not fullscreen_enabled

                                if fullscreen_enabled:
                                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                                else:
                                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

                            elif game_pause_back_button.is_clicked(event):
                                game_pause_screen = "MENU"

                        else:
                            if game_resume_button.is_clicked(event):
                                game_paused = False
                                game_pause_screen = "MENU"

                            elif game_pause_settings_button.is_clicked(event):
                                game_pause_screen = "SETTINGS"

                            elif game_forfeit_button.is_clicked(event):
                                client.send({
                                    "type": FORFEIT,
                                    "session_id": session_id,
                                    "room_id": room_id,
                                    "payload": {}
                                })

                                game_paused = False
                                game_pause_screen = "MENU"
                                status_text = "Forfeit sent"

                    elif game_pause_button.is_clicked(event):
                        game_paused = True
                        game_pause_screen = "MENU"

                    elif current_turn_session_id == session_id:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        grid_x = (mouse_x - GAME_ENEMY_BOARD_X) // CELL_SIZE
                        grid_y = (mouse_y - GAME_ENEMY_BOARD_Y) // CELL_SIZE

                        if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                            client.send({
                                "type": FIRE,
                                "session_id": session_id,
                                "room_id": room_id,
                                "payload": {
                                    "x": grid_x,
                                    "y": grid_y
                                }
                            })

                elif screen_state == "SPECTATOR":
                    if spectator_paused:
                        if spectator_pause_screen == "SETTINGS":
                            if settings_sound_button.is_clicked(event):
                                sound_enabled = not sound_enabled
                                apply_music_volume()

                            elif settings_volume_down_button.is_clicked(event):
                                volume = max(0, volume - 10)
                                apply_music_volume()

                            elif settings_volume_up_button.is_clicked(event):
                                volume = min(100, volume + 10)
                                apply_music_volume()

                            elif settings_fullscreen_button.is_clicked(event):
                                fullscreen_enabled = not fullscreen_enabled

                                if fullscreen_enabled:
                                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                                else:
                                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

                            elif spectator_pause_back_button.is_clicked(event):
                                spectator_pause_screen = "MENU"

                        else:
                            if spectator_resume_button.is_clicked(event):
                                spectator_paused = False
                                spectator_pause_screen = "MENU"

                            elif spectator_settings_button.is_clicked(event):
                                spectator_pause_screen = "SETTINGS"

                            elif spectator_main_menu_button.is_clicked(event):
                                leave_current_room()
                                spectator_paused = False
                                spectator_pause_screen = "MENU"

                    elif spectator_pause_button.is_clicked(event):
                        spectator_paused = True
                        spectator_pause_screen = "MENU"


        current_time = pygame.time.get_ticks()

        if (
            session_id
            and latency_auto_enabled
            and not game_paused
            and current_time - last_ping_time >= PING_INTERVAL_MS
        ):
            last_ping_time = current_time

            client.send({
                "type": PING,
                "session_id": session_id,
                "payload": {
                    "sent_at": current_time
                }
            })


        switch_music_if_needed()

        if screen_state == "TITLE":
            draw_title_screen()
        elif screen_state == "AUTH":
            draw_auth_screen()
        elif screen_state == "MAIN_MENU":
            draw_main_menu()
        elif screen_state == "ROOM_WAITING":
            draw_room_waiting()
        elif screen_state == "ROOM_BROWSER":
            draw_room_browser()
            if selected_room_index is not None:
                draw_room_join_popup()
        elif screen_state == "CREATE_ROOM":
            draw_create_room()
        elif screen_state == "SETTINGS":
            draw_settings()
        elif screen_state == "PLACEMENT":
            draw_placement()
        elif screen_state == "GAME":
            draw_game()
        elif screen_state == "SPECTATOR_WAITING":
            draw_spectator_waiting()
        elif screen_state == "SPECTATOR":
            draw_spectator()
        elif screen_state == "SPECTATOR_RESULT":
            draw_spectator_result()
        elif screen_state == "REPLAY_VIEWER":
            draw_replay_viewer()
        elif screen_state == "LEADERBOARD":
            draw_leaderboard()
        elif screen_state == "REPLAY_LIST":
            draw_replay_list()
        elif screen_state == "REPLAY_DETAIL":
            draw_replay_detail()
        elif screen_state == "GAME_OVER":
            draw_game_over()

        pygame.display.flip()
        clock.tick(60)

    stop_music()
    client.close()
    pygame.quit()
