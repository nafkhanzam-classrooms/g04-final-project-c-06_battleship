import uuid

from server.game_room import GameRoom


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_waiting_room(self, player_1):
        room_id = str(uuid.uuid4())[:8]

        room = GameRoom(
            room_id=room_id,
            player_1=player_1,
            player_2=None,
            room_name=f"Quick Play {room_id}",
            password=""
        )

        self.rooms[room_id] = room
        return room

    def create_manual_room(self, player_1, room_name, password=""):
        room_id = str(uuid.uuid4())[:8]

        room = GameRoom(
            room_id=room_id,
            player_1=player_1,
            player_2=None,
            room_name=room_name,
            password=password
        )

        self.rooms[room_id] = room
        return room

    def create_room(self, player_1, player_2):
        room_id = str(uuid.uuid4())[:8]

        room = GameRoom(
            room_id=room_id,
            player_1=player_1,
            player_2=player_2,
            room_name=f"Match {room_id}",
            password=""
        )

        self.rooms[room_id] = room
        return room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def get_waiting_room(self):
        for room in self.rooms.values():
            if room.status == "WAITING_OPPONENT" and len(room.players) == 1:
                return room

        return None

    def get_room_list(self):
        return [
            room.get_public_info()
            for room in self.rooms.values()
            if room.status in ["WAITING_OPPONENT", "WAITING_PLACEMENT", "IN_GAME"]
            and len(room.players) > 0
        ]

    def join_room_as_player(self, room_id, player, password=""):
        room = self.get_room(room_id)

        if not room:
            return False, "Room not found", None

        if not room.is_password_valid(password):
            return False, "Wrong room password", None

        if room.status not in ["WAITING_OPPONENT"]:
            return False, "Room is not available for player join", None

        success, info = room.add_player(player)

        if not success:
            return False, info, None

        return True, info, room

    def join_room_as_spectator(self, room_id, spectator, password=""):
        room = self.get_room(room_id)

        if not room:
            return False, "Room not found", None

        if not room.is_password_valid(password):
            return False, "Wrong room password", None

        room.add_spectator(spectator)

        return True, "Joined as spectator", room

    def remove_user_from_room(self, room_id, session_id):
        room = self.get_room(room_id)

        if not room:
            return None

        room.remove_user(session_id)

        if room.status == "EMPTY" or (len(room.players) == 0 and len(room.spectators) == 0):
            del self.rooms[room_id]
            return None

        return room