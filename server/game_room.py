from shared.constants import BOARD_SIZE, CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS


class GameRoom:
    def __init__(self, room_id, player_1, player_2=None, room_name=None, password=""):
        self.room_id = room_id
        self.room_name = room_name or f"Room-{room_id}"
        self.password = password or ""
        self.host_session_id = player_1["session_id"]
        self.players = [player_1]

        if player_2 is not None:
            self.players.append(player_2)

        self.spectators = []
        self.status = "WAITING_OPPONENT" if player_2 is None else "WAITING_PLACEMENT"

        self.boards = {
            player_1["session_id"]: self.create_empty_board()
        }

        if player_2 is not None:
            self.boards[player_2["session_id"]] = self.create_empty_board()

        self.shots = {
            player_1["session_id"]: self.create_empty_board()
        }

        if player_2 is not None:
            self.shots[player_2["session_id"]] = self.create_empty_board()

        self.ready_players = set()
        self.current_turn = None
        self.winner = None
        self.turn_number = 0
        self.ship_layouts = {}

    def create_empty_board(self):
        return [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def get_player_index(self, session_id):
        for index, player in enumerate(self.players):
            if player["session_id"] == session_id:
                return index
        return None

    def get_player(self, session_id):
        for player in self.players:
            if player["session_id"] == session_id:
                return player
        return None

    def get_opponent(self, session_id):
        for player in self.players:
            if player["session_id"] != session_id:
                return player
        return None

    def add_player(self, player):
        if len(self.players) >= 2:
            return False, "Room is full"

        self.players.append(player)
        self.boards[player["session_id"]] = self.create_empty_board()
        self.shots[player["session_id"]] = self.create_empty_board()
        self.status = "WAITING_PLACEMENT"

        return True, "Player joined room"

    def add_spectator(self, spectator):
        self.spectators.append(spectator)

    def is_password_valid(self, password):
        if not self.password:
            return True

        return self.password == password


    def get_public_info(self):
        player_names = [player["username"] for player in self.players]

        return {
            "room_id": self.room_id,
            "room_name": self.room_name,
            "status": self.status,
            "players": [player["username"] for player in self.players],
            "player_count": len(self.players),
            "spectator_count": len(self.spectators),
            "has_password": bool(self.password),
            "host_session_id": self.host_session_id,
            "is_quickplay": self.room_name.startswith("Quick Play")
        }

    def get_public_board(self, session_id):
        board = self.boards[session_id]
        public_board = self.create_empty_board()

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if board[y][x] == CELL_HIT:
                    public_board[y][x] = CELL_HIT
                elif board[y][x] == CELL_MISS:
                    public_board[y][x] = CELL_MISS

        return public_board

    def get_spectator_board(self, session_id):
        board = self.boards.get(session_id)

        if board is None:
            return self.create_empty_board()

        spectator_board = self.create_empty_board()

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                spectator_board[y][x] = board[y][x]

        # Tambahin indikator MISS dari shot board lawan.
        # Board target hanya menyimpan ship/hit, sedangkan miss disimpan di shots milik shooter.
        opponent = self.get_opponent(session_id)

        if opponent:
            opponent_shots = self.shots.get(opponent["session_id"])

            if opponent_shots:
                for y in range(BOARD_SIZE):
                    for x in range(BOARD_SIZE):
                        if opponent_shots[y][x] == CELL_MISS:
                            spectator_board[y][x] = CELL_MISS

        return spectator_board

    def remove_user(self, session_id):
        removed = False

        original_player_count = len(self.players)
        original_spectator_count = len(self.spectators)

        self.players = [
            player for player in self.players
            if player["session_id"] != session_id
        ]

        self.spectators = [
            spectator for spectator in self.spectators
            if spectator["session_id"] != session_id
        ]

        if len(self.players) != original_player_count:
            removed = True

        if len(self.spectators) != original_spectator_count:
            removed = True

        if session_id in self.boards:
            del self.boards[session_id]
            removed = True

        if session_id in self.shots:
            del self.shots[session_id]
            removed = True

        if session_id in self.ready_players:
            self.ready_players.remove(session_id)
            removed = True

        if session_id in self.ship_layouts:
            del self.ship_layouts[session_id]
            removed = True

        if self.current_turn == session_id:
            self.current_turn = None

        if len(self.players) == 0:
            self.status = "EMPTY"

        elif len(self.players) == 1:
            self.status = "WAITING_OPPONENT"
            self.current_turn = None
            self.ready_players.clear()

        elif len(self.players) == 2 and self.status != "IN_GAME":
            self.status = "WAITING_PLACEMENT"

        return removed

    def place_ships(self, session_id, ships):
        board = self.create_empty_board()

        for ship in ships:
            cells = ship.get("cells", [])

            for cell in cells:
                x = cell.get("x")
                y = cell.get("y")

                if not self.is_inside_board(x, y):
                    return False, "Ship cell is outside board"

                if board[y][x] == CELL_SHIP:
                    return False, "Ships overlap"

            for cell in cells:
                x = cell["x"]
                y = cell["y"]
                board[y][x] = CELL_SHIP

        self.boards[session_id] = board
        self.ship_layouts[session_id] = ships
        return True, "Ships placed successfully"

    def get_ship_layout(self, session_id):
        return self.ship_layouts.get(session_id, [])


    def reset_for_rematch_request(self, session_id):
        requester = self.get_player(session_id)

        if requester is None:
            return False, "Player not found"

        self.players = [requester]
        self.host_session_id = requester["session_id"]
        self.status = "WAITING_OPPONENT"

        self.boards = {
            requester["session_id"]: self.create_empty_board()
        }
        self.shots = {
            requester["session_id"]: self.create_empty_board()
        }

        self.ready_players.clear()
        self.current_turn = None
        self.winner = None
        self.turn_number = 0
        self.ship_layouts = {}

        return True, "Waiting for rematch opponent"


    def set_ready(self, session_id):
        self.ready_players.add(session_id)

        if len(self.ready_players) == 2:
            self.status = "IN_GAME"
            self.current_turn = self.players[0]["session_id"]
            return True

        return False

    def fire(self, shooter_session_id, x, y):
        if self.status != "IN_GAME":
            return False, "Game is not running", None

        if shooter_session_id != self.current_turn:
            return False, "Not your turn", None

        if not self.is_inside_board(x, y):
            return False, "Shot is outside board", None

        opponent = self.get_opponent(shooter_session_id)

        if opponent is None:
            return False, "Opponent not found", None

        opponent_session_id = opponent["session_id"]
        opponent_board = self.boards[opponent_session_id]
        shooter_shots = self.shots[shooter_session_id]

        if shooter_shots[y][x] in [CELL_HIT, CELL_MISS]:
            return False, "You already fired at this cell", None

        if opponent_board[y][x] == CELL_SHIP:
            result = "HIT"
            opponent_board[y][x] = CELL_HIT
            shooter_shots[y][x] = CELL_HIT
        else:
            result = "MISS"
            shooter_shots[y][x] = CELL_MISS

        winner_session_id = None

        if self.is_all_ships_destroyed(opponent_session_id):
            self.status = "FINISHED"
            self.winner = shooter_session_id
            winner_session_id = shooter_session_id
        else:
            self.current_turn = opponent_session_id

        self.turn_number += 1

        fire_data = {
            "turn_number": self.turn_number,
            "x": x,
            "y": y,
            "result": result,
            "next_turn_session_id": self.current_turn,
            "winner_session_id": winner_session_id
        }

        return True, "Fire processed", fire_data

    def is_all_ships_destroyed(self, session_id):
        board = self.boards[session_id]

        for row in board:
            for cell in row:
                if cell == CELL_SHIP:
                    return False

        return True

    def is_inside_board(self, x, y):
        return (
            isinstance(x, int)
            and isinstance(y, int)
            and 0 <= x < BOARD_SIZE
            and 0 <= y < BOARD_SIZE
        )