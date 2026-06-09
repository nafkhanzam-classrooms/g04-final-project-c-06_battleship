import pygame
import sys

from client.network_client import NetworkClient
from client.ui.ui_config import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, BACKGROUND_IMAGE
from client.ui.components import (
    Button,
    TextInput,
    draw_center_text,
    draw_panel,
    draw_background
)
from client.ui.theme import COLORS

from shared.constants import BOARD_SIZE, SHIPS, CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS
from shared.message_type import (
    LOGIN,
    LOGIN_SUCCESS,
    REGISTER,
    REGISTER_SUCCESS,
    REGISTER_FAILED,
    LOGIN_FAILED,
    ROOM_WAITING_CREATED,
    CREATE_ROOM,
    CREATE_ROOM_SUCCESS,
    CREATE_ROOM_FAILED,
    GET_ROOM_LIST,
    ROOM_LIST_DATA,
    JOIN_ROOM,
    JOIN_ROOM_SUCCESS,
    JOIN_ROOM_FAILED,
    LEAVE_ROOM,
    ROOM_UPDATED,
    PING,
    PONG,
    MATCHMAKE,
    MATCH_FOUND,
    WAITING_FOR_PLAYER,
    START_PLACEMENT,
    PLACEMENT_START,
    PLACE_SHIPS,
    PLACE_SHIPS_SUCCESS,
    PLACE_SHIPS_ERROR,
    READY,
    WAITING_OPPONENT_READY,
    GAME_START,
    FIRE,
    FIRE_RESULT,
    OPPONENT_FIRE_RESULT,
    TURN_UPDATE,
    GAME_OVER,
    REMATCH_REQUEST,
    REMATCH_WAITING,
    REMATCH_MATCHED,
    FORFEIT,
    JOIN_SPECTATOR,
    SPECTATOR_JOINED,
    SPECTATOR_UPDATE,
    GET_LEADERBOARD,
    LEADERBOARD_DATA,
    GET_REPLAY_LIST,
    REPLAY_LIST_DATA,
    GET_REPLAY_DETAIL,
    REPLAY_DETAIL_DATA,
    ERROR
)

from client import assets as client_assets
from client import audio as client_audio
from client import game_logic as client_game_logic
from client import screens as client_screens
from client import message_handler as client_message_handler
from client import event_handler as client_event_handler



def bind_module_functions(module):
    for name in dir(module):
        if name.startswith("_"):
            continue

        value = getattr(module, name)

        if callable(value):
            try:
                value = type(value)(value.__code__, globals(), value.__name__, value.__defaults__, value.__closure__)
            except AttributeError:
                pass

            globals()[name] = value


bind_module_functions(client_assets)
bind_module_functions(client_audio)
bind_module_functions(client_game_logic)
bind_module_functions(client_screens)
bind_module_functions(client_message_handler)
bind_module_functions(client_event_handler)

pygame.init()

try:
    pygame.mixer.init()
except pygame.error:
    pass

WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

HEADER_FONT_PATH = "client/assets/fonts/PirataOne-Regular.ttf"
UI_FONT_PATH = "client/assets/fonts/JollyRoger-Regular.ttf"




font = load_font(UI_FONT_PATH, 28)
title_font = load_font(HEADER_FONT_PATH, 72)
small_font = load_font(UI_FONT_PATH, 22)

clock = pygame.time.Clock()
client = NetworkClient()



ship_images = load_ship_images()

username = ""
session_id = None
room_id = None
opponent_username = None
player_index = None
latency_ms = None
latency_auto_enabled = False
last_ping_time = 0
PING_INTERVAL_MS = 2000
status_text = "Click anywhere to start"

screen_state = "TITLE"
game_paused = False
game_pause_screen = "MENU"

placed_ships = []
current_ship_index = 0
orientation = "H"
placement_confirm_open = False

local_board = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
enemy_board = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

ships_submitted = False
current_turn_session_id = None
winner_session_id = None

leaderboard_data = []
leaderboard_mode = "TOP"
leaderboard_scroll_offset = 0
replay_list = []
selected_replay = None
replay_step_index = 0
replay_source_state = "MAIN_MENU"

available_rooms = []
selected_room_index = None
filtered_rooms = []
selected_room = None
room_browser_status = "Press Refresh to load rooms"
current_spectator_count = 0
spectator_room_status = "WAITING_OPPONENT"

is_spectator = False
spectator_player_1 = None
spectator_player_2 = None
spectator_board_1 = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
spectator_board_2 = [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
spectator_ships_1 = []
spectator_ships_2 = []
spectator_paused = False
spectator_pause_screen = "MENU"

sound_enabled = True
volume = 50
fullscreen_enabled = False

MUSIC_MAIN_PATH = "client/assets/music/main_music.mp3"
MUSIC_BATTLE_PATH = "client/assets/music/battle_music.mp3"
MUSIC_MAIN_SECRET_PATH = "client/assets/music/main_music_secret.mp3"
MUSIC_BATTLE_SECRET_PATH = "client/assets/music/battle_music_secret.mp3"
EASTER_EGG_SOUND_PATH = "client/assets/music/kode_berhasil.mp3"

current_music_type = None
music_available = True
secret_music_enabled = False
easter_code_buffer = ""
easter_popup_open = False
easter_pending_secret_state = None
easter_popup_text = ":)"

CELL_SIZE = 40

PLACEMENT_PANEL_WIDTH = 980
PLACEMENT_PANEL_HEIGHT = 610
PLACEMENT_PANEL_X = (WIDTH - PLACEMENT_PANEL_WIDTH) // 2
PLACEMENT_PANEL_Y = 55

PLACEMENT_BOARD_X = PLACEMENT_PANEL_X + 90
PLACEMENT_BOARD_Y = PLACEMENT_PANEL_Y + 125

MY_BOARD_X = 60
MY_BOARD_Y = 160

ENEMY_BOARD_X = 560
ENEMY_BOARD_Y = 160

GAME_PANEL_WIDTH = 1180
GAME_PANEL_HEIGHT = 610
GAME_PANEL_X = (WIDTH - GAME_PANEL_WIDTH) // 2
GAME_PANEL_Y = 55

GAME_MY_BOARD_X = GAME_PANEL_X + 80
GAME_MY_BOARD_Y = GAME_PANEL_Y + 165

GAME_ENEMY_BOARD_X = GAME_PANEL_X + 700
GAME_ENEMY_BOARD_Y = GAME_PANEL_Y + 165


# ---------- UI ELEMENTS ----------

AUTH_PANEL_WIDTH = 420
AUTH_PANEL_HEIGHT = 360
AUTH_PANEL_X = (WIDTH - AUTH_PANEL_WIDTH) // 2
AUTH_PANEL_Y = 165

AUTH_INPUT_WIDTH = 300
AUTH_INPUT_HEIGHT = 45
AUTH_INPUT_X = AUTH_PANEL_X + (AUTH_PANEL_WIDTH - AUTH_INPUT_WIDTH) // 2

username_input = TextInput(
    AUTH_INPUT_X,
    AUTH_PANEL_Y + 95,
    AUTH_INPUT_WIDTH,
    AUTH_INPUT_HEIGHT,
    small_font,
    "Username"
)

password_input = TextInput(
    AUTH_INPUT_X,
    AUTH_PANEL_Y + 155,
    AUTH_INPUT_WIDTH,
    AUTH_INPUT_HEIGHT,
    small_font,
    "Password",
    password=True
)

login_button = Button(
    AUTH_INPUT_X,
    AUTH_PANEL_Y + 225,
    140,
    45,
    "Login",
    small_font
)

register_button = Button(
    AUTH_INPUT_X + 160,
    AUTH_PANEL_Y + 225,
    140,
    45,
    "Register",
    small_font
)

MAIN_BUTTON_WIDTH = 280
MAIN_BUTTON_HEIGHT = 50
MAIN_BUTTON_X = (WIDTH - MAIN_BUTTON_WIDTH) // 2

quick_play_button = Button(MAIN_BUTTON_X, 180, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Quick Play", small_font)
play_button = Button(MAIN_BUTTON_X, 245, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Play / Room List", small_font)
leaderboard_button = Button(MAIN_BUTTON_X, 310, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Leaderboard", small_font)
settings_button = Button(MAIN_BUTTON_X, 375, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Settings", small_font)
exit_button = Button(MAIN_BUTTON_X, 440, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Exit", small_font)

room_start_button = Button(MAIN_BUTTON_X, 460, MAIN_BUTTON_WIDTH, 50, "Start / Continue", small_font, enabled=False)
room_spectate_button = Button(MAIN_BUTTON_X, 525, MAIN_BUTTON_WIDTH, 50, "Switch Spectate/Main", small_font)

settings_sound_button = Button(MAIN_BUTTON_X, 230, MAIN_BUTTON_WIDTH, 45, "Sound: ON", small_font)
settings_volume_down_button = Button(MAIN_BUTTON_X, 295, 130, 45, "Volume -", small_font)
settings_volume_up_button = Button(MAIN_BUTTON_X + 150, 295, 130, 45, "Volume +", small_font)
settings_fullscreen_button = Button(MAIN_BUTTON_X, 360, MAIN_BUTTON_WIDTH, 45, "Windowed", small_font)
settings_back_button = Button(MAIN_BUTTON_X, 425, MAIN_BUTTON_WIDTH, 45, "Back", small_font)

room_search_input = TextInput((WIDTH - 420) // 2, 140, 420, 45, small_font, "Search room name")
create_room_button = Button((WIDTH // 2) - 260, 560, 150, 45, "Create", small_font)
refresh_room_button = Button((WIDTH // 2) - 75, 560, 150, 45, "Refresh", small_font)
room_back_button = Button((WIDTH // 2) + 110, 560, 150, 45, "Back", small_font)

join_room_buttons = []
join_as_player_button = Button(0, 0, 200, 45, "As Player", small_font)
join_as_spectator_button = Button(0, 0, 220, 45, "As Spectator", small_font)
join_cancel_button = Button(0, 0, 180, 45, "Cancel", small_font)
popup_password_input = TextInput(0, 0, 320, 45, small_font, "Room password")
refresh_room_button = Button((WIDTH // 2) - 260, 560, 150, 45, "Refresh", small_font)
create_room_button = Button((WIDTH // 2) - 80, 560, 150, 45, "Create", small_font)
room_back_button = Button((WIDTH // 2) + 100, 560, 150, 45, "Back", small_font)

join_room_buttons = []
join_as_player_button = Button(0, 0, 200, 45, "As Player", small_font)
join_as_spectator_button = Button(0, 0, 220, 45, "As Spectator", small_font)
join_cancel_button = Button(0, 0, 180, 45, "Cancel", small_font)

create_room_name_input = TextInput((WIDTH - 360) // 2, 250, 360, 45, small_font, "Room name")
create_room_password_input = TextInput((WIDTH - 360) // 2, 315, 360, 45, small_font, "Password optional", password=True)
create_room_submit_button = Button((WIDTH // 2) - 170, 430, 150, 45, "Create", small_font)
create_room_cancel_button = Button((WIDTH // 2) + 20, 430, 150, 45, "Cancel", small_font)

placement_confirm_yes_button = Button(0, 0, 160, 45, "YES", small_font)
placement_confirm_no_button = Button(0, 0, 160, 45, "NO / EDIT", small_font)

game_pause_button = Button(0, 0, 110, 42, "Pause", small_font)
game_resume_button = Button(0, 0, 220, 48, "RESUME", small_font)
game_pause_settings_button = Button(0, 0, 220, 48, "SETTINGS", small_font)
game_forfeit_button = Button(0, 0, 220, 48, "FORFEIT", small_font)
game_pause_back_button = Button(0, 0, 220, 48, "BACK", small_font)
spectator_pause_button = Button(0, 0, 120, 42, "Pause", small_font)
spectator_resume_button = Button(0, 0, 220, 48, "RESUME", small_font)
spectator_settings_button = Button(0, 0, 220, 48, "SETTINGS", small_font)
spectator_main_menu_button = Button(0, 0, 220, 48, "MAIN MENU", small_font)
spectator_pause_back_button = Button(0, 0, 220, 48, "BACK", small_font)
game_over_rematch_button = Button(0, 0, 220, 48, "REMATCH", small_font)
game_over_replay_button = Button(0, 0, 220, 48, "REPLAY", small_font)
game_over_main_menu_button = Button(0, 0, 220, 48, "MAIN MENU", small_font)

spectator_continue_button = Button(0, 0, 220, 48, "CONTINUE", small_font)
spectator_result_replay_button = Button(0, 0, 220, 48, "REPLAY", small_font)
spectator_result_main_menu_button = Button(0, 0, 220, 48, "MAIN MENU", small_font)

replay_prev_button = Button(0, 0, 150, 45, "PREV", small_font)
replay_next_button = Button(0, 0, 150, 45, "NEXT", small_font)
replay_exit_button = Button(0, 0, 180, 45, "MAIN MENU", small_font)
leaderboard_back_button = Button(0, 0, 180, 45, "BACK", small_font)
leaderboard_my_stat_button = Button(0, 0, 180, 45, "MY STAT", small_font)
leaderboard_top_button = Button(0, 0, 180, 45, "TOP 10", small_font)
easter_next_button = Button(0, 0, 180, 45, "NEXT", small_font)


# ---------- BASIC HELPERS ----------





























































































































# ---------- DRAW SCREENS ----------


client.on_message = handle_server_message

try:
    client.connect()
except ConnectionRefusedError:
    print("Server belum jalan. Jalankan: python -m server.main")
    pygame.quit()
    sys.exit()

run_loop()
