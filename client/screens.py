import pygame

from shared.constants import BOARD_SIZE, CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS
from client.ui.theme import COLORS


def draw_text(text, x, y, font_obj=None, color=(255, 255, 255)):
    if font_obj is None:
        font_obj = font

    surface = font_obj.render(str(text), True, color)
    screen.blit(surface, (x, y))


def draw_right_text(text, right_x, y, font_obj=None, color=(255, 255, 255)):
    if font_obj is None:
        font_obj = font

    surface = font_obj.render(str(text), True, color)
    rect = surface.get_rect(topright=(right_x, y))
    screen.blit(surface, rect)


def draw_grid(board, start_x, start_y, show_ships=True):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(
                start_x + x * CELL_SIZE,
                start_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            cell = board[y][x]

            if cell == CELL_SHIP and show_ships:
                color = (80, 130, 180)
            elif cell == CELL_HIT:
                color = (200, 60, 60)
            elif cell == CELL_MISS:
                color = (180, 180, 180)
            else:
                color = (30, 60, 90)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def draw_grid_with_labels(board, start_x, start_y, show_ships=True):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    for x in range(BOARD_SIZE):
        label_x = start_x + x * CELL_SIZE + 14
        label_y = start_y - 30
        draw_text(letters[x], label_x, label_y, small_font, COLORS["text_muted"])

    for y in range(BOARD_SIZE):
        label_x = start_x - 38
        label_y = start_y + y * CELL_SIZE + 10
        draw_text(str(y + 1), label_x, label_y, small_font, COLORS["text_muted"])

    draw_grid(board, start_x, start_y, show_ships)


def draw_ship_asset(ship_name, cells, orient="H", alpha=255, board_x=None, board_y=None):
    if board_x is None:
        board_x = PLACEMENT_BOARD_X

    if board_y is None:
        board_y = PLACEMENT_BOARD_Y

    image = ship_images.get(ship_name)

    if image is None or not cells:
        return False

    min_x, min_y, max_x, max_y = get_ship_bounds(cells)
    target_width = (max_x - min_x + 1) * CELL_SIZE
    target_height = (max_y - min_y + 1) * CELL_SIZE

    image_to_draw = image.copy()

    if orient == "V":
        image_to_draw = pygame.transform.rotate(image_to_draw, -90)

    image_to_draw = pygame.transform.scale(image_to_draw, (target_width, target_height))
    image_to_draw.set_alpha(alpha)

    draw_x = board_x + min_x * CELL_SIZE
    draw_y = board_y + min_y * CELL_SIZE
    screen.blit(image_to_draw, (draw_x, draw_y))

    return True


def draw_placed_ship_assets():
    for placed_ship in placed_ships:
        draw_ship_asset(
            placed_ship["name"],
            placed_ship["cells"],
            placed_ship.get("orientation", "H"),
            alpha=255
        )


def draw_ship_ghost():
    if screen_state != "PLACEMENT":
        return

    if placement_confirm_open:
        return

    if current_ship_index >= len(SHIPS):
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = (mouse_x - PLACEMENT_BOARD_X) // CELL_SIZE
    grid_y = (mouse_y - PLACEMENT_BOARD_Y) // CELL_SIZE

    if grid_x < 0 or grid_x >= BOARD_SIZE or grid_y < 0 or grid_y >= BOARD_SIZE:
        return

    ship = SHIPS[current_ship_index]
    cells = get_ship_cells(grid_x, grid_y, ship, orientation)
    valid = can_place_ship(cells)

    image_drawn = False
    if valid:
        image_drawn = draw_ship_asset(ship["name"], cells, orientation, alpha=165)

    ghost_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    if valid:
        ghost_color = (80, 220, 140, 95)
        border_color = (120, 255, 180, 220)
    else:
        ghost_color = (220, 70, 70, 125)
        border_color = (255, 120, 120, 230)

    for cell in cells:
        x = cell["x"]
        y = cell["y"]

        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            rect = pygame.Rect(
                PLACEMENT_BOARD_X + x * CELL_SIZE,
                PLACEMENT_BOARD_Y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            if not image_drawn:
                pygame.draw.rect(ghost_surface, ghost_color, rect)

            pygame.draw.rect(ghost_surface, border_color, rect, 2)

    screen.blit(ghost_surface, (0, 0))


def draw_placement_confirm_popup():
    if not placement_confirm_open:
        return

    popup_width = 520
    popup_height = 240
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    draw_panel(screen, popup_x, popup_y, popup_width, popup_height)

    draw_center_text(
        screen,
        "CONFIRM PLACEMENT",
        popup_y + 45,
        font,
        (255, 235, 190)
    )

    draw_center_text(
        screen,
        "Are you sure with this ship placement?",
        popup_y + 95,
        small_font,
        COLORS["text_muted"]
    )

    placement_confirm_yes_button.rect.x = popup_x + 85
    placement_confirm_yes_button.rect.y = popup_y + 145

    placement_confirm_no_button.rect.x = popup_x + 275
    placement_confirm_no_button.rect.y = popup_y + 145

    placement_confirm_yes_button.draw(screen)
    placement_confirm_no_button.draw(screen)


def draw_grid_lines(start_x, start_y):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(
                start_x + x * CELL_SIZE,
                start_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (210, 220, 230), rect, 1)


def draw_board_base_water(start_x, start_y):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(
                start_x + x * CELL_SIZE,
                start_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (30, 60, 90), rect)


def draw_hit_miss_overlay(board, start_x, start_y):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            cell = board[y][x]

            center_x_pos = start_x + x * CELL_SIZE + CELL_SIZE // 2
            center_y_pos = start_y + y * CELL_SIZE + CELL_SIZE // 2

            if cell == CELL_HIT:
                pygame.draw.circle(screen, (215, 55, 55), (center_x_pos, center_y_pos), 14)

            elif cell == CELL_MISS:
                pygame.draw.circle(screen, (205, 210, 220), (center_x_pos, center_y_pos), 7)
                pygame.draw.circle(screen, (60, 75, 95), (center_x_pos, center_y_pos), 7, 2)


def draw_board_labels(start_x, start_y):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    for x in range(BOARD_SIZE):
        label_x = start_x + x * CELL_SIZE + 14
        label_y = start_y - 30
        draw_text(letters[x], label_x, label_y, small_font, COLORS["text_muted"])

    for y in range(BOARD_SIZE):
        label_x = start_x - 30
        label_y = start_y + y * CELL_SIZE + 10
        draw_text(str(y + 1), label_x, label_y, small_font, COLORS["text_muted"])


def draw_own_game_board():
    draw_board_labels(GAME_MY_BOARD_X, GAME_MY_BOARD_Y)
    draw_board_base_water(GAME_MY_BOARD_X, GAME_MY_BOARD_Y)

    for placed_ship in placed_ships:
        draw_ship_asset(
            placed_ship["name"],
            placed_ship["cells"],
            placed_ship.get("orientation", "H"),
            alpha=255,
            board_x=GAME_MY_BOARD_X,
            board_y=GAME_MY_BOARD_Y
        )

    draw_hit_miss_overlay(local_board, GAME_MY_BOARD_X, GAME_MY_BOARD_Y)
    draw_grid_lines(GAME_MY_BOARD_X, GAME_MY_BOARD_Y)


def draw_enemy_target_hover():
    if current_turn_session_id != session_id:
        return

    if game_paused:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    grid_x = (mouse_x - GAME_ENEMY_BOARD_X) // CELL_SIZE
    grid_y = (mouse_y - GAME_ENEMY_BOARD_Y) // CELL_SIZE

    if not (0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE):
        return

    rect = pygame.Rect(
        GAME_ENEMY_BOARD_X + grid_x * CELL_SIZE,
        GAME_ENEMY_BOARD_Y + grid_y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    hover_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(hover_surface, (90, 210, 140, 90), rect)
    pygame.draw.rect(hover_surface, (140, 255, 190, 230), rect, 3)
    screen.blit(hover_surface, (0, 0))


def draw_enemy_game_board():
    draw_board_labels(GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)
    draw_board_base_water(GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)
    draw_enemy_target_hover()
    draw_hit_miss_overlay(enemy_board, GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)
    draw_grid_lines(GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)


def draw_game_side_panel():
    panel_x = GAME_PANEL_X + 505
    panel_y = GAME_PANEL_Y + 160
    panel_w = 150
    panel_h = 400

    pygame.draw.rect(
        screen,
        COLORS["panel_light"],
        pygame.Rect(panel_x, panel_y, panel_w, panel_h),
        border_radius=14
    )

    def draw_center_in_panel(text_value, y, font_obj, color):
        surface = font_obj.render(str(text_value), True, color)
        rect = surface.get_rect(center=(panel_x + panel_w // 2, y))
        screen.blit(surface, rect)

    draw_center_in_panel("BATTLE", panel_y + 40, font, (255, 235, 190))

    if current_turn_session_id == session_id:
        turn_text = "YOUR TURN"
        turn_color = COLORS["success"]
    else:
        turn_text = "WAIT"
        turn_color = COLORS["warning"]

    draw_center_in_panel(turn_text, panel_y + 95, small_font, turn_color)

    my_hits, my_misses = get_board_stats(enemy_board)
    enemy_hits, enemy_misses = get_board_stats(local_board)

    stat_x = panel_x + 28

    draw_text("Your shots", stat_x, panel_y + 145, small_font, (255, 235, 190))
    draw_text(f"Hit  : {my_hits}", stat_x, panel_y + 180, small_font)
    draw_text(f"Miss : {my_misses}", stat_x, panel_y + 210, small_font)

    draw_text("Enemy shots", stat_x, panel_y + 265, small_font, (255, 235, 190))
    draw_text(f"Hit  : {enemy_hits}", stat_x, panel_y + 300, small_font)
    draw_text(f"Miss : {enemy_misses}", stat_x, panel_y + 330, small_font)

    hint = "Click enemy" if current_turn_session_id == session_id else "Please wait"
    draw_center_in_panel(hint, panel_y + 375, small_font, COLORS["text_muted"])


def draw_pause_overlay_background():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))


def draw_game_pause_menu():
    draw_pause_overlay_background()

    panel_width = 420
    panel_height = 360
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)
    draw_center_text(screen, "PAUSED", panel_y + 60, font, (255, 235, 190))

    button_x = panel_x + (panel_width - game_resume_button.rect.width) // 2

    game_resume_button.rect.x = button_x
    game_resume_button.rect.y = panel_y + 110

    game_pause_settings_button.rect.x = button_x
    game_pause_settings_button.rect.y = panel_y + 175

    game_forfeit_button.rect.x = button_x
    game_forfeit_button.rect.y = panel_y + 240

    game_resume_button.draw(screen)
    game_pause_settings_button.draw(screen)
    game_forfeit_button.draw(screen)

    draw_center_text(
        screen,
        "Forfeit gives the opponent an instant win",
        panel_y + 320,
        small_font,
        COLORS["text_muted"]
    )


def draw_game_pause_settings():
    draw_pause_overlay_background()

    panel_width = 420
    panel_height = 420
    panel_x = center_x(panel_width)
    panel_y = 130

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "SETTINGS", panel_y + 45, font, (255, 235, 190))

    settings_sound_button.text = f"Sound: {'ON' if sound_enabled else 'OFF'}"
    settings_fullscreen_button.text = "Fullscreen" if fullscreen_enabled else "Windowed"

    draw_center_text(screen, f"Volume: {volume}", panel_y + 85, small_font, COLORS["text_muted"])

    button_x = panel_x + (panel_width - MAIN_BUTTON_WIDTH) // 2

    settings_sound_button.rect.x = button_x
    settings_sound_button.rect.y = panel_y + 110

    settings_volume_down_button.rect.x = button_x
    settings_volume_down_button.rect.y = panel_y + 175

    settings_volume_up_button.rect.x = button_x + 150
    settings_volume_up_button.rect.y = panel_y + 175

    settings_fullscreen_button.rect.x = button_x
    settings_fullscreen_button.rect.y = panel_y + 240

    game_pause_back_button.rect.width = MAIN_BUTTON_WIDTH
    game_pause_back_button.rect.height = 45
    game_pause_back_button.rect.x = button_x
    game_pause_back_button.rect.y = panel_y + 305

    settings_sound_button.draw(screen)
    settings_volume_down_button.draw(screen)
    settings_volume_up_button.draw(screen)
    settings_fullscreen_button.draw(screen)
    game_pause_back_button.draw(screen)


def draw_game_pause_overlay():
    if not game_paused:
        return

    if game_pause_screen == "SETTINGS":
        draw_game_pause_settings()
    else:
        draw_game_pause_menu()


def draw_replay_board(board, ships, start_x, start_y):
    draw_board_labels(start_x, start_y)
    draw_board_base_water(start_x, start_y)

    for ship in ships:
        draw_ship_asset(
            ship["name"],
            ship["cells"],
            ship.get("orientation", "H"),
            alpha=255,
            board_x=start_x,
            board_y=start_y
        )

    if not ships:
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if board[y][x] == CELL_SHIP:
                    rect = pygame.Rect(
                        start_x + x * CELL_SIZE,
                        start_y + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(screen, (80, 130, 180), rect)

    draw_hit_miss_overlay(board, start_x, start_y)
    draw_grid_lines(start_x, start_y)


def draw_easter_popup():
    if not easter_popup_open:
        return

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    panel_width = 360
    panel_height = 240
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(
        screen,
        easter_popup_text,
        panel_y + 85,
        title_font,
        (255, 235, 190)
    )

    easter_next_button.rect.x = panel_x + (panel_width - easter_next_button.rect.width) // 2
    easter_next_button.rect.y = panel_y + 150
    easter_next_button.draw(screen)


def draw_title_screen():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 480
    panel_height = 300
    panel_x = (WIDTH - panel_width) // 2
    panel_y = 170

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(
        screen,
        "BATTLESHIP",
        panel_y + 75,
        title_font,
        (255, 235, 190)
    )

    draw_center_text(
        screen,
        "Click anywhere to start",
        panel_y + 165,
        small_font,
        COLORS["text_muted"]
    )

    draw_center_text(
        screen,
        "Multiplayer Battleship Board Game",
        panel_y + 205,
        small_font,
        COLORS["text_muted"]
    )


def draw_auth_screen():
    draw_background(screen, BACKGROUND_IMAGE)

    draw_panel(
        screen,
        AUTH_PANEL_X,
        AUTH_PANEL_Y,
        AUTH_PANEL_WIDTH,
        AUTH_PANEL_HEIGHT
    )

    draw_center_text(
        screen,
        "Login / Register",
        AUTH_PANEL_Y + 45,
        font,
        (255, 235, 190)
    )

    username_input.draw(screen)
    password_input.draw(screen)

    login_button.draw(screen)
    register_button.draw(screen)

    draw_center_text(
        screen,
        status_text,
        AUTH_PANEL_Y + 315,
        small_font,
        COLORS["text_muted"]
    )


def draw_main_menu():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 430
    panel_height = 490
    panel_x = center_x(panel_width)
    panel_y = 95

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "MAIN MENU", panel_y + 55, title_font, (255, 235, 190))
    draw_center_text(screen, f"Logged in as: {username}", panel_y + 90, small_font, COLORS["text_muted"])

    button_x = panel_x + (panel_width - MAIN_BUTTON_WIDTH) // 2

    quick_play_button.rect.x = button_x
    quick_play_button.rect.y = panel_y + 125

    play_button.rect.x = button_x
    play_button.rect.y = panel_y + 190

    leaderboard_button.rect.x = button_x
    leaderboard_button.rect.y = panel_y + 255

    settings_button.rect.x = button_x
    settings_button.rect.y = panel_y + 320

    exit_button.rect.x = button_x
    exit_button.rect.y = panel_y + 385

    quick_play_button.draw(screen)
    play_button.draw(screen)
    leaderboard_button.draw(screen)
    settings_button.draw(screen)
    exit_button.draw(screen)

    draw_center_text(screen, status_text, panel_y + 455, small_font, COLORS["text_muted"])

    draw_easter_popup()


def draw_room_waiting():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 560
    panel_height = 520
    panel_x = center_x(panel_width)
    panel_y = 90

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "ROOM", panel_y + 45, title_font, (255, 235, 190))

    content_x = panel_x + 70

    draw_text(f"Room ID: {room_id}", content_x, panel_y + 115, small_font)
    draw_text(f"You: {username}", content_x, panel_y + 155, small_font)
    draw_text(f"Opponent: {opponent_username}", content_x, panel_y + 195, small_font)
    draw_text(f"Player Index: {player_index}", content_x, panel_y + 235, small_font)
    draw_text(f"Latency: {latency_ms} ms", content_x, panel_y + 275, small_font)
    draw_text(f"Status: {status_text}", content_x, panel_y + 315, small_font, COLORS["text_muted"])

    room_start_button.rect.x = panel_x + (panel_width - room_start_button.rect.width) // 2
    room_start_button.rect.y = panel_y + 380

    room_spectate_button.rect.x = panel_x + (panel_width - room_spectate_button.rect.width) // 2
    room_spectate_button.rect.y = panel_y + 445

    room_start_button.enabled = opponent_username is not None
    room_start_button.draw(screen)
    room_spectate_button.draw(screen)

    if not room_start_button.enabled:
        draw_center_text(screen, "Start aktif kalau musuh sudah ada", panel_y + 360, small_font, COLORS["warning"])


def draw_room_browser():
    global join_room_buttons

    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 980
    panel_height = 610
    panel_x = (WIDTH - panel_width) // 2
    panel_y = 55

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "ROOM LIST", panel_y + 45, title_font, (255, 235, 190))

    room_search_input.rect.x = panel_x + (panel_width - room_search_input.rect.width) // 2
    room_search_input.rect.y = panel_y + 105
    room_search_input.draw(screen)

    visible_rooms = filter_rooms()

    header_y = panel_y + 175
    draw_text("Room", panel_x + 70, header_y, small_font, COLORS["text_muted"])
    draw_text("Status", panel_x + 250, header_y, small_font, COLORS["text_muted"])
    draw_text("Access", panel_x + 390, header_y, small_font, COLORS["text_muted"])
    draw_text("Players", panel_x + 520, header_y, small_font, COLORS["text_muted"])
    draw_text("Spectators", panel_x + 650, header_y, small_font, COLORS["text_muted"])

    join_room_buttons = []

    start_y = panel_y + 220
    row_height = 50

    if not visible_rooms:
        draw_text("No rooms found", panel_x + 70, start_y, small_font, COLORS["text_muted"])
    else:
        for index, room in enumerate(visible_rooms[:7]):
            row_y = start_y + index * row_height

            if room.get("is_quickplay"):
                room_display = room.get("room_id", "-")
            else:
                room_display = room.get("room_name", room.get("room_id", "-"))
            status = format_room_status(room)
            access = format_room_lock(room)
            player_count = room.get("player_count", 0)
            spectator_count = room.get("spectator_count", 0)

            draw_text(room_display, panel_x + 70, row_y + 8, small_font)
            draw_text(status, panel_x + 250, row_y + 8, small_font)
            draw_text(access, panel_x + 390, row_y + 8, small_font)
            draw_text(f"{player_count}/2", panel_x + 520, row_y + 8, small_font)
            draw_text(str(spectator_count), panel_x + 650, row_y + 8, small_font)

            join_button = Button(
                panel_x + 785,
                row_y,
                110,
                38,
                "Join",
                small_font
            )
            join_button.draw(screen)

            join_room_buttons.append({
                "button": join_button,
                "room": room
            })

    draw_center_text(
        screen,
        room_browser_status,
        panel_y + 500,
        small_font,
        COLORS["text_muted"]
    )

    refresh_room_button.rect.x = panel_x + 210
    refresh_room_button.rect.y = panel_y + 545

    create_room_button.rect.x = panel_x + 415
    create_room_button.rect.y = panel_y + 545

    room_back_button.rect.x = panel_x + 620
    room_back_button.rect.y = panel_y + 545

    refresh_room_button.draw(screen)
    create_room_button.draw(screen)
    room_back_button.draw(screen)


def draw_room_join_popup():
    if selected_room_index is None:
        return

    visible_rooms = filter_rooms()

    if selected_room_index >= len(visible_rooms):
        return

    room = visible_rooms[selected_room_index]

    popup_width = 580
    popup_height = 300 if room.get("has_password") else 240
    popup_x = (WIDTH - popup_width) // 2
    popup_y = 230

    draw_panel(screen, popup_x, popup_y, popup_width, popup_height)

    room_id_value = room.get("room_id", "-")
    status = format_room_status(room)
    access = format_room_lock(room)
    player_count = room.get("player_count", 0)
    spectator_count = room.get("spectator_count", 0)

    draw_center_text(screen, "JOIN ROOM", popup_y + 40, font, (255, 235, 190))

    draw_center_text(
        screen,
        f"{room_id_value} | {status} | {access} | Players {player_count}/2 | Spectators {spectator_count}",
        popup_y + 85,
        small_font,
        COLORS["text_muted"]
    )

    button_y = popup_y + 135

    if room.get("has_password"):
        popup_password_input.rect.x = popup_x + (popup_width - popup_password_input.rect.width) // 2
        popup_password_input.rect.y = popup_y + 125
        popup_password_input.draw(screen)
        button_y = popup_y + 185

    join_as_player_button.rect.x = popup_x + 60
    join_as_player_button.rect.y = button_y

    join_as_spectator_button.rect.x = popup_x + 300
    join_as_spectator_button.rect.y = button_y

    join_cancel_button.rect.x = popup_x + 200
    join_cancel_button.rect.y = button_y + 60

    join_as_player_button.draw(screen)
    join_as_spectator_button.draw(screen)
    join_cancel_button.draw(screen)


def draw_create_room():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 520
    panel_height = 380
    panel_x = (WIDTH - panel_width) // 2
    panel_y = 150

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "CREATE ROOM", panel_y + 50, font, (255, 235, 190))

    create_room_name_input.rect.x = panel_x + (panel_width - create_room_name_input.rect.width) // 2
    create_room_name_input.rect.y = panel_y + 110
    create_room_name_input.draw(screen)

    create_room_password_input.rect.x = panel_x + (panel_width - create_room_password_input.rect.width) // 2
    create_room_password_input.rect.y = panel_y + 170
    create_room_password_input.draw(screen)

    create_room_submit_button.rect.x = panel_x + 85
    create_room_submit_button.rect.y = panel_y + 250

    create_room_cancel_button.rect.x = panel_x + 275
    create_room_cancel_button.rect.y = panel_y + 250

    create_room_submit_button.draw(screen)
    create_room_cancel_button.draw(screen)

    draw_center_text(
        screen,
        status_text,
        panel_y + 325,
        small_font,
        COLORS["text_muted"]
    )


def draw_settings():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 420
    panel_height = 420
    panel_x = center_x(panel_width)
    panel_y = 130

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "SETTINGS", panel_y + 45, font, (255, 235, 190))

    settings_sound_button.text = f"Sound: {'ON' if sound_enabled else 'OFF'}"
    settings_fullscreen_button.text = "Fullscreen" if fullscreen_enabled else "Windowed"

    draw_center_text(screen, f"Volume: {volume}", panel_y + 85, small_font, COLORS["text_muted"])

    button_x = panel_x + (panel_width - MAIN_BUTTON_WIDTH) // 2

    settings_sound_button.rect.x = button_x
    settings_sound_button.rect.y = panel_y + 110

    settings_volume_down_button.rect.x = button_x
    settings_volume_down_button.rect.y = panel_y + 175

    settings_volume_up_button.rect.x = button_x + 150
    settings_volume_up_button.rect.y = panel_y + 175

    settings_fullscreen_button.rect.x = button_x
    settings_fullscreen_button.rect.y = panel_y + 240

    settings_back_button.rect.x = button_x
    settings_back_button.rect.y = panel_y + 305

    settings_sound_button.draw(screen)
    settings_volume_down_button.draw(screen)
    settings_volume_up_button.draw(screen)
    settings_fullscreen_button.draw(screen)
    settings_back_button.draw(screen)


def draw_placement():
    draw_background(screen, BACKGROUND_IMAGE)

    draw_panel(
        screen,
        PLACEMENT_PANEL_X,
        PLACEMENT_PANEL_Y,
        PLACEMENT_PANEL_WIDTH,
        PLACEMENT_PANEL_HEIGHT
    )

    draw_center_text(
        screen,
        "SHIP PLACEMENT",
        PLACEMENT_PANEL_Y + 45,
        title_font,
        (255, 235, 190)
    )

    draw_grid_with_labels(
        local_board,
        PLACEMENT_BOARD_X,
        PLACEMENT_BOARD_Y,
        show_ships=True
    )

    draw_placed_ship_assets()
    draw_ship_ghost()

    info_x = PLACEMENT_PANEL_X + 600
    info_y = PLACEMENT_PANEL_Y + 125

    draw_text("Placement Info", info_x, info_y, font, (255, 235, 190))

    if current_ship_index < len(SHIPS):
        ship = SHIPS[current_ship_index]
        ship_width, ship_height = get_ship_dimensions(ship, orientation)

        draw_text(f"Current Ship: {ship['name']}", info_x, info_y + 55, small_font)
        draw_text(f"Size: {ship_width}x{ship_height}", info_x, info_y + 90, small_font)
    else:
        draw_text("All ships placed", info_x, info_y + 55, small_font, COLORS["success"])
        draw_text("Ready to submit", info_x, info_y + 90, small_font, COLORS["text_muted"])

    draw_text(f"Orientation: {orientation}", info_x, info_y + 135, small_font)
    draw_text(f"Placed: {len(placed_ships)}/{len(SHIPS)}", info_x, info_y + 170, small_font)

    draw_text("Controls", info_x, info_y + 235, font, (255, 235, 190))
    draw_text("Click board = Place ship", info_x, info_y + 285, small_font)
    draw_text("R = Rotate ghost", info_x, info_y + 320, small_font)
    draw_text("Z = Undo last ship", info_x, info_y + 355, small_font)
    draw_text("ENTER = Open confirm", info_x, info_y + 390, small_font)

    draw_text(
        f"Status: {status_text}",
        PLACEMENT_PANEL_X + 70,
        PLACEMENT_PANEL_Y + 555,
        small_font,
        COLORS["text_muted"]
    )

    draw_placement_confirm_popup()


def draw_game_info_box():
    box_width = 520
    box_height = 78
    box_x = GAME_PANEL_X + (GAME_PANEL_WIDTH - box_width) // 2
    box_y = GAME_PANEL_Y + 20

    pygame.draw.rect(
        screen,
        COLORS["panel_light"],
        pygame.Rect(box_x, box_y, box_width, box_height),
        border_radius=14
    )
    pygame.draw.rect(
        screen,
        COLORS["input_border"],
        pygame.Rect(box_x, box_y, box_width, box_height),
        width=2,
        border_radius=14
    )

    left_x = box_x + 35
    right_x = box_x + 285

    draw_text("You", left_x, box_y + 10, small_font, (255, 235, 190))
    draw_text(str(username), left_x + 105, box_y + 10, small_font, COLORS["text_muted"])

    draw_text("Opponent", left_x, box_y + 42, small_font, (255, 235, 190))
    draw_text(str(opponent_username), left_x + 105, box_y + 42, small_font, COLORS["text_muted"])

    draw_text("Room ID", right_x, box_y + 10, small_font, (255, 235, 190))
    draw_text(str(room_id), right_x + 115, box_y + 10, small_font, COLORS["text_muted"])

    draw_text("Latency", right_x, box_y + 42, small_font, (255, 235, 190))
    draw_text(get_latency_display(), right_x + 115, box_y + 42, small_font, COLORS["text_muted"])


def draw_game():
    draw_background(screen, BACKGROUND_IMAGE)

    draw_panel(
        screen,
        GAME_PANEL_X,
        GAME_PANEL_Y,
        GAME_PANEL_WIDTH,
        GAME_PANEL_HEIGHT
    )

    draw_game_info_box()

    # Headings are lifted slightly so they do not collide with board labels.
    draw_text(
        "YOUR FLEET",
        GAME_MY_BOARD_X,
        GAME_MY_BOARD_Y - 85,
        font,
        (255, 235, 190)
    )

    enemy_title_right_x = GAME_ENEMY_BOARD_X + BOARD_SIZE * CELL_SIZE
    draw_right_text(
        "ENEMY WATERS",
        enemy_title_right_x,
        GAME_ENEMY_BOARD_Y - 85,
        font,
        (255, 235, 190)
    )

    draw_own_game_board()
    draw_enemy_game_board()
    draw_game_side_panel()

    if current_turn_session_id == session_id:
        instruction = "Your turn - click enemy board to fire"
        instruction_color = COLORS["success"]
    else:
        instruction = "Opponent turn - wait for your turn"
        instruction_color = COLORS["warning"]

    bottom_y = GAME_PANEL_Y + 585

    draw_center_text(
        screen,
        instruction,
        bottom_y,
        small_font,
        instruction_color
    )

    draw_text(
        f"Spectators: {current_spectator_count}",
        GAME_PANEL_X + 80,
        bottom_y,
        small_font,
        COLORS["text_muted"]
    )

    game_pause_button.rect.x = GAME_PANEL_X + GAME_PANEL_WIDTH - 140
    game_pause_button.rect.y = GAME_PANEL_Y + 25
    game_pause_button.draw(screen)

    draw_game_pause_overlay()


def draw_spectator_waiting():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 560
    panel_height = 430
    panel_x = center_x(panel_width)
    panel_y = 120

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "SPECTATOR", panel_y + 50, title_font, (255, 235, 190))

    content_x = panel_x + 70

    draw_text(f"Room ID: {room_id}", content_x, panel_y + 125, small_font)
    draw_text(f"Player 1: {spectator_player_1}", content_x, panel_y + 165, small_font)
    draw_text(f"Player 2: {spectator_player_2}", content_x, panel_y + 205, small_font)
    draw_text(f"Spectators: {current_spectator_count}", content_x, panel_y + 245, small_font)
    draw_text(f"Status: {status_text}", content_x, panel_y + 285, small_font, COLORS["text_muted"])

    if spectator_room_status == "WAITING_PLACEMENT":
        popup_width = 300
        popup_height = 90
        popup_x = (WIDTH - popup_width) // 2
        popup_y = panel_y + 320

        draw_panel(screen, popup_x, popup_y, popup_width, popup_height)
        draw_center_text(screen, "Loading...", popup_y + 48, font, (255, 235, 190))
    else:
        draw_center_text(screen, "Waiting for the game to start", panel_y + 345, small_font, COLORS["warning"])


def draw_spectator_board(board, ships, start_x, start_y):
    draw_board_labels(start_x, start_y)
    draw_board_base_water(start_x, start_y)

    for ship in ships:
        draw_ship_asset(
            ship["name"],
            ship["cells"],
            ship.get("orientation", "H"),
            alpha=255,
            board_x=start_x,
            board_y=start_y
        )

    # Fallback if the server has not sent ship assets yet.
    if not ships:
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if board[y][x] == CELL_SHIP:
                    rect = pygame.Rect(
                        start_x + x * CELL_SIZE,
                        start_y + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(screen, (80, 130, 180), rect)

    draw_hit_miss_overlay(board, start_x, start_y)
    draw_grid_lines(start_x, start_y)


def draw_spectator_pause_menu():
    draw_pause_overlay_background()

    panel_width = 420
    panel_height = 360
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)
    draw_center_text(screen, "PAUSE", panel_y + 60, font, (255, 235, 190))

    button_x = panel_x + (panel_width - spectator_resume_button.rect.width) // 2

    spectator_resume_button.rect.x = button_x
    spectator_resume_button.rect.y = panel_y + 110

    spectator_settings_button.rect.x = button_x
    spectator_settings_button.rect.y = panel_y + 175

    spectator_main_menu_button.rect.x = button_x
    spectator_main_menu_button.rect.y = panel_y + 240

    spectator_resume_button.draw(screen)
    spectator_settings_button.draw(screen)
    spectator_main_menu_button.draw(screen)


def draw_spectator_pause_settings():
    draw_pause_overlay_background()

    panel_width = 420
    panel_height = 420
    panel_x = center_x(panel_width)
    panel_y = 130

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "SETTINGS", panel_y + 45, font, (255, 235, 190))

    settings_sound_button.text = f"Sound: {'ON' if sound_enabled else 'OFF'}"
    settings_fullscreen_button.text = "Fullscreen" if fullscreen_enabled else "Windowed"

    draw_center_text(screen, f"Volume: {volume}", panel_y + 85, small_font, COLORS["text_muted"])

    button_x = panel_x + (panel_width - MAIN_BUTTON_WIDTH) // 2

    settings_sound_button.rect.x = button_x
    settings_sound_button.rect.y = panel_y + 110

    settings_volume_down_button.rect.x = button_x
    settings_volume_down_button.rect.y = panel_y + 175

    settings_volume_up_button.rect.x = button_x + 150
    settings_volume_up_button.rect.y = panel_y + 175

    settings_fullscreen_button.rect.x = button_x
    settings_fullscreen_button.rect.y = panel_y + 240

    spectator_pause_back_button.rect.width = MAIN_BUTTON_WIDTH
    spectator_pause_back_button.rect.height = 45
    spectator_pause_back_button.rect.x = button_x
    spectator_pause_back_button.rect.y = panel_y + 305

    settings_sound_button.draw(screen)
    settings_volume_down_button.draw(screen)
    settings_volume_up_button.draw(screen)
    settings_fullscreen_button.draw(screen)
    spectator_pause_back_button.draw(screen)


def draw_spectator_pause_overlay():
    if not spectator_paused:
        return

    if spectator_pause_screen == "SETTINGS":
        draw_spectator_pause_settings()
    else:
        draw_spectator_pause_menu()


def draw_spectator():
    draw_background(screen, BACKGROUND_IMAGE)

    draw_panel(
        screen,
        GAME_PANEL_X,
        GAME_PANEL_Y,
        GAME_PANEL_WIDTH,
        GAME_PANEL_HEIGHT
    )

    # Room name above the center battle box.
    draw_center_text(
        screen,
        f"Room: {room_id}",
        GAME_PANEL_Y + 85,
        small_font,
        COLORS["text_muted"]
    )

    draw_text(
        f"{spectator_player_1}",
        GAME_MY_BOARD_X,
        GAME_MY_BOARD_Y - 85,
        font,
        (255, 235, 190)
    )

    enemy_title_right_x = GAME_ENEMY_BOARD_X + BOARD_SIZE * CELL_SIZE
    draw_right_text(
        f"{spectator_player_2}",
        enemy_title_right_x,
        GAME_ENEMY_BOARD_Y - 85,
        font,
        (255, 235, 190)
    )

    draw_spectator_board(spectator_board_1, spectator_ships_1, GAME_MY_BOARD_X, GAME_MY_BOARD_Y)
    draw_spectator_board(spectator_board_2, spectator_ships_2, GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)

    draw_game_side_panel()

    spectator_pause_button.rect.x = GAME_PANEL_X + GAME_PANEL_WIDTH - 140
    spectator_pause_button.rect.y = GAME_PANEL_Y + 25
    spectator_pause_button.draw(screen)

    draw_center_text(
        screen,
        status_text,
        GAME_PANEL_Y + 585,
        small_font,
        COLORS["text_muted"]
    )

    draw_spectator_pause_overlay()


def draw_game_over():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 440
    panel_height = 390
    panel_x = center_x(panel_width)
    panel_y = 150

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    if winner_session_id == session_id:
        result_text = "You Win!"
    else:
        result_text = "You Lose!"

    draw_center_text(screen, result_text, panel_y + 70, title_font, (255, 235, 190))

    button_x = panel_x + (panel_width - game_over_rematch_button.rect.width) // 2

    game_over_rematch_button.rect.x = button_x
    game_over_rematch_button.rect.y = panel_y + 145

    game_over_replay_button.rect.x = button_x
    game_over_replay_button.rect.y = panel_y + 210

    game_over_main_menu_button.rect.x = button_x
    game_over_main_menu_button.rect.y = panel_y + 275

    game_over_rematch_button.draw(screen)
    game_over_replay_button.draw(screen)
    game_over_main_menu_button.draw(screen)


def draw_spectator_result():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 460
    panel_height = 390
    panel_x = center_x(panel_width)
    panel_y = 150

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    winner_name = "Player"
    if selected_replay and selected_replay.get("winner"):
        winner_name = selected_replay.get("winner")
    elif status_text:
        winner_name = status_text.replace("Game over", "").strip() or "Player"

    draw_center_text(screen, f"{winner_name} WIN", panel_y + 70, title_font, (255, 235, 190))

    button_x = panel_x + (panel_width - spectator_continue_button.rect.width) // 2

    spectator_continue_button.rect.x = button_x
    spectator_continue_button.rect.y = panel_y + 145

    spectator_result_replay_button.rect.x = button_x
    spectator_result_replay_button.rect.y = panel_y + 210

    spectator_result_main_menu_button.rect.x = button_x
    spectator_result_main_menu_button.rect.y = panel_y + 275

    spectator_continue_button.draw(screen)
    spectator_result_replay_button.draw(screen)
    spectator_result_main_menu_button.draw(screen)


def draw_replay_viewer():
    draw_background(screen, BACKGROUND_IMAGE)

    draw_panel(
        screen,
        GAME_PANEL_X,
        GAME_PANEL_Y,
        GAME_PANEL_WIDTH,
        GAME_PANEL_HEIGHT
    )

    if not selected_replay:
        draw_center_text(screen, "Replay not found", HEIGHT // 2, font, COLORS["warning"])
        return

    ships_1 = selected_replay.get("player_1_ships", [])
    ships_2 = selected_replay.get("player_2_ships", [])

    board_1 = build_replay_board(selected_replay, 1, replay_step_index)
    board_2 = build_replay_board(selected_replay, 2, replay_step_index)

    draw_replay_board(board_1, ships_1, GAME_MY_BOARD_X, GAME_MY_BOARD_Y)
    draw_replay_board(board_2, ships_2, GAME_ENEMY_BOARD_X, GAME_ENEMY_BOARD_Y)

    total_events = len(selected_replay.get("events", []))

    draw_center_text(
        screen,
        f"Replay {replay_step_index}/{total_events}",
        GAME_PANEL_Y + 95,
        font,
        (255, 235, 190)
    )

    replay_prev_button.rect.x = (WIDTH // 2) - 250
    replay_prev_button.rect.y = GAME_PANEL_Y + 570

    replay_next_button.rect.x = (WIDTH // 2) - 75
    replay_next_button.rect.y = GAME_PANEL_Y + 570

    replay_exit_button.rect.x = (WIDTH // 2) + 100
    replay_exit_button.rect.y = GAME_PANEL_Y + 570

    replay_prev_button.enabled = replay_step_index > 0
    replay_next_button.enabled = replay_step_index < total_events

    replay_prev_button.draw(screen)
    replay_next_button.draw(screen)
    replay_exit_button.draw(screen)


def draw_leaderboard_row(rank, player, x, y, row_width, highlight=False):
    row_rect = pygame.Rect(x, y, row_width, 42)

    if highlight:
        row_color = (70, 95, 125)
    elif rank % 2 == 0:
        row_color = (36, 58, 82)
    else:
        row_color = (28, 48, 72)

    pygame.draw.rect(screen, row_color, row_rect, border_radius=10)
    pygame.draw.rect(screen, (120, 140, 160), row_rect, 1, border_radius=10)

    draw_text(str(rank), x + 20, y + 9, small_font, COLORS["text_muted"])
    draw_text(player.get("username", "-"), x + 85, y + 9, small_font)
    draw_text(str(player.get("win", 0)), x + 330, y + 9, small_font, COLORS["success"])
    draw_text(str(player.get("lose", 0)), x + 430, y + 9, small_font, COLORS["warning"])
    draw_text(str(player.get("total_match", 0)), x + 535, y + 9, small_font)
    draw_text(f"{player.get('win_rate', 0)}%", x + 650, y + 9, small_font)


def draw_my_stat_card(player, panel_x, panel_y):
    card_w = 560
    card_h = 270
    card_x = panel_x + 130
    card_y = panel_y + 150

    pygame.draw.rect(screen, COLORS["panel_light"], pygame.Rect(card_x, card_y, card_w, card_h), border_radius=18)
    pygame.draw.rect(screen, COLORS["input_border"], pygame.Rect(card_x, card_y, card_w, card_h), 2, border_radius=18)

    draw_center_text(screen, player.get("username", username), card_y + 45, font, (255, 235, 190))

    left_x = card_x + 70
    right_x = card_x + 325
    y = card_y + 95

    draw_text(f"Matches : {player.get('total_match', 0)}", left_x, y, small_font)
    draw_text(f"Wins    : {player.get('win', 0)}", left_x, y + 45, small_font, COLORS["success"])
    draw_text(f"Loses   : {player.get('lose', 0)}", left_x, y + 90, small_font, COLORS["warning"])

    draw_text(f"Hits    : {player.get('hit_count', 0)}", right_x, y, small_font)
    draw_text(f"Misses  : {player.get('miss_count', 0)}", right_x, y + 45, small_font)
    draw_text(f"Winrate : {player.get('win_rate', 0)}%", right_x, y + 90, small_font, (255, 235, 190))


def draw_leaderboard():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 900
    panel_height = 570
    panel_x = center_x(panel_width)
    panel_y = 65

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    title = "MY STAT" if leaderboard_mode == "MY_STAT" else "LEADERBOARD"
    subtitle = "Your statistic" if leaderboard_mode == "MY_STAT" else "Top 10 by total wins"

    draw_center_text(screen, title, panel_y + 45, title_font, (255, 235, 190))
    draw_center_text(screen, subtitle, panel_y + 92, small_font, COLORS["text_muted"])

    button_y = panel_y + 505
    button_gap = 24
    button_width = 180
    total_button_width = (button_width * 2) + button_gap
    button_start_x = panel_x + (panel_width - total_button_width) // 2

    leaderboard_back_button.rect.width = button_width
    leaderboard_my_stat_button.rect.width = button_width
    leaderboard_top_button.rect.width = button_width

    leaderboard_back_button.rect.x = button_start_x
    leaderboard_back_button.rect.y = button_y

    leaderboard_my_stat_button.rect.x = button_start_x + button_width + button_gap
    leaderboard_my_stat_button.rect.y = button_y
    leaderboard_top_button.rect.x = button_start_x + button_width + button_gap
    leaderboard_top_button.rect.y = button_y

    if leaderboard_mode == "MY_STAT":
        active_button = leaderboard_top_button
    else:
        active_button = leaderboard_my_stat_button

    if leaderboard_mode == "MY_STAT":
        player = get_my_leaderboard_stat()

        card_w = 520
        card_h = 255
        card_x = panel_x + (panel_width - card_w) // 2
        card_y = panel_y + 155

        pygame.draw.rect(screen, COLORS["panel_light"], pygame.Rect(card_x, card_y, card_w, card_h), border_radius=18)
        pygame.draw.rect(screen, COLORS["input_border"], pygame.Rect(card_x, card_y, card_w, card_h), 2, border_radius=18)

        draw_center_text(screen, player.get("username", username), card_y + 45, font, (255, 235, 190))

        left_x = card_x + 85
        right_x = card_x + 300
        stat_y = card_y + 100

        draw_text(f"Matches : {player.get('total_match', 0)}", left_x, stat_y, small_font)
        draw_text(f"Wins    : {player.get('win', 0)}", left_x, stat_y + 42, small_font, COLORS["success"])
        draw_text(f"Loses   : {player.get('lose', 0)}", left_x, stat_y + 84, small_font, COLORS["warning"])

        draw_text(f"Hits    : {player.get('hit_count', 0)}", right_x, stat_y, small_font)
        draw_text(f"Misses  : {player.get('miss_count', 0)}", right_x, stat_y + 42, small_font)
        draw_text(f"Winrate : {player.get('win_rate', 0)}%", right_x, stat_y + 84, small_font, (255, 235, 190))

    else:
        content_x = panel_x + 70
        header_y = panel_y + 135
        row_width = panel_width - 140

        draw_text("Rank", content_x + 15, header_y, small_font, COLORS["text_muted"])
        draw_text("Username", content_x + 85, header_y, small_font, COLORS["text_muted"])
        draw_text("Win", content_x + 330, header_y, small_font, COLORS["text_muted"])
        draw_text("Lose", content_x + 430, header_y, small_font, COLORS["text_muted"])
        draw_text("Match", content_x + 535, header_y, small_font, COLORS["text_muted"])
        draw_text("Win Rate", content_x + 650, header_y, small_font, COLORS["text_muted"])

        sorted_players = sorted(
            leaderboard_data,
            key=lambda player: (
                player.get("win", 0),
                player.get("hit_count", 0),
                player.get("total_match", 0)
            ),
            reverse=True
        )[:10]

        max_visible_rows = 6
        max_offset = max(0, len(sorted_players) - max_visible_rows)
        start_index = min(max(0, leaderboard_scroll_offset), max_offset)
        visible_players = sorted_players[start_index:start_index + max_visible_rows]

        if not sorted_players:
            draw_center_text(screen, "No leaderboard data", panel_y + 260, small_font, COLORS["text_muted"])
        else:
            y = panel_y + 170
            for visible_index, player in enumerate(visible_players):
                real_rank = start_index + visible_index + 1
                draw_leaderboard_row(
                    real_rank,
                    player,
                    content_x,
                    y,
                    row_width,
                    highlight=player.get("username") == username
                )
                y += 48

            if len(sorted_players) > max_visible_rows:
                draw_center_text(
                    screen,
                    f"Scroll mouse wheel  {start_index + 1}-{start_index + len(visible_players)} / {len(sorted_players)}",
                    panel_y + 470,
                    small_font,
                    COLORS["text_muted"]
                )

    leaderboard_back_button.draw(screen)
    active_button.draw(screen)


def draw_replay_list():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 900
    panel_height = 540
    panel_x = center_x(panel_width)
    panel_y = 80

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "REPLAY LIST", panel_y + 45, title_font, (255, 235, 190))
    draw_center_text(screen, "Press 1-9 to open replay | ESC to menu", panel_y + 90, small_font, COLORS["text_muted"])

    content_x = panel_x + 55
    y = panel_y + 135

    if not replay_list:
        draw_text("No replay found", content_x, y, small_font)
        return

    for index, replay in enumerate(replay_list[:9]):
        line = (
            f"{index + 1}. Room {replay['room_id']} | "
            f"{replay['player_1']} vs {replay['player_2']} | "
            f"Winner: {replay['winner']} | "
            f"Events: {replay['total_events']}"
        )

        draw_text(line, content_x, y, small_font)
        y += 35


def draw_replay_detail():
    draw_background(screen, BACKGROUND_IMAGE)

    panel_width = 900
    panel_height = 540
    panel_x = center_x(panel_width)
    panel_y = 80

    draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

    draw_center_text(screen, "REPLAY DETAIL", panel_y + 45, title_font, (255, 235, 190))
    draw_center_text(screen, "ESC to menu", panel_y + 90, small_font, COLORS["text_muted"])

    content_x = panel_x + 55

    if not selected_replay:
        draw_text("No replay selected", content_x, panel_y + 135, small_font)
        return

    draw_text(
        f"{selected_replay['player_1']} vs {selected_replay['player_2']}",
        content_x,
        panel_y + 135,
        small_font
    )
    draw_text(f"Winner: {selected_replay['winner']}", content_x, panel_y + 165, small_font)

    y = panel_y + 215
    for event in selected_replay["events"][:12]:
        line = (
            f"Turn {event['turn']}: "
            f"{event['shooter']} fired ({event['x']}, {event['y']}) "
            f"= {event['result']}"
        )

        draw_text(line, content_x, y, small_font)
        y += 28
