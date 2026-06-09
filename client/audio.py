import pygame


def get_music_type_for_state(state):
    battle_states = [
        "GAME",
        "GAME_OVER",
        "SPECTATOR",
        "SPECTATOR_RESULT",
        "REPLAY_VIEWER"
    ]

    if state in battle_states:
        return "BATTLE"

    return "MAIN"


def get_music_path(music_type):
    if secret_music_enabled:
        if music_type == "BATTLE":
            return MUSIC_BATTLE_SECRET_PATH

        return MUSIC_MAIN_SECRET_PATH

    if music_type == "BATTLE":
        return MUSIC_BATTLE_PATH

    return MUSIC_MAIN_PATH


def apply_music_volume():
    if not pygame.mixer.get_init():
        return

    if sound_enabled:
        pygame.mixer.music.set_volume(volume / 100)
    else:
        pygame.mixer.music.set_volume(0)


def switch_music_if_needed():
    global current_music_type, music_available

    if not pygame.mixer.get_init():
        return

    target_music_type = get_music_type_for_state(screen_state)

    if current_music_type == target_music_type:
        apply_music_volume()
        return

    music_path = get_music_path(target_music_type)

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        apply_music_volume()
        pygame.mixer.music.play(-1)
        current_music_type = target_music_type
        music_available = True
    except pygame.error:
        current_music_type = None
        music_available = False


def stop_music():
    global current_music_type

    if not pygame.mixer.get_init():
        return

    pygame.mixer.music.stop()
    current_music_type = None


def force_music_refresh():
    global current_music_type

    current_music_type = None
    switch_music_if_needed()


def play_easter_sound():
    if not pygame.mixer.get_init():
        return

    try:
        sound = pygame.mixer.Sound(EASTER_EGG_SOUND_PATH)
        sound.set_volume(volume / 100 if sound_enabled else 0)
        sound.play()
    except pygame.error:
        pass


def trigger_easter_code():
    global easter_popup_open, easter_pending_secret_state, easter_popup_text

    easter_pending_secret_state = not secret_music_enabled
    easter_popup_open = True
    easter_popup_text = ":)" if easter_pending_secret_state else ":("

    play_easter_sound()


def handle_easter_key(event):
    global easter_code_buffer

    if screen_state != "MAIN_MENU":
        easter_code_buffer = ""
        return

    if event.key < 32 or event.key > 126:
        return

    char = event.unicode

    if not char:
        return

    easter_code_buffer = (easter_code_buffer + char.upper())[-7:]

    if easter_code_buffer == "HESOYAM":
        easter_code_buffer = ""
        trigger_easter_code()
