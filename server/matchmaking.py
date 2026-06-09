class Matchmaking:
    def __init__(self, room_manager):
        self.room_manager = room_manager

    def join_queue(self, player):
        waiting_room = self.room_manager.get_waiting_room()

        if waiting_room is None:
            room = self.room_manager.create_waiting_room(player)
            return room, False

        success, info = waiting_room.add_player(player)

        if not success:
            room = self.room_manager.create_waiting_room(player)
            return room, False

        return waiting_room, True