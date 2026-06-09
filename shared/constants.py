HOST = "127.0.0.1"
PORT = 5000

BOARD_SIZE = 10

CELL_EMPTY = 0
CELL_SHIP = 1
CELL_HIT = 2
CELL_MISS = 3

SHIPS = [
    {
        "name": "Wooden Boat",
        "width": 1,
        "height": 2,
        "image": "client/assets/ships/wooden_boat.png"
    },
    {
        "name": "Pirate Boat",
        "width": 2,
        "height": 2,
        "image": "client/assets/ships/pirate_boat.png"
    },
    {
        "name": "Battle Ship",
        "width": 2,
        "height": 4,
        "image": "client/assets/ships/battle_ship.png"
    },
    {
        "name": "Steel Ship",
        "width": 1,
        "height": 3,
        "image": "client/assets/ships/steel_ship.png"
    },
    {
        "name": "Cyber Ship",
        "width": 1,
        "height": 3,
        "image": "client/assets/ships/cyber_ship.png"
    },
]