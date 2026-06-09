from shared.constants import BOARD_SIZE, CELL_EMPTY


def create_empty_board():
    return [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
