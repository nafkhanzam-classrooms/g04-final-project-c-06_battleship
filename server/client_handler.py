import json
import socket
import threading

from shared.serializer import encode_message, decode_message
from server.response_builder import ok, error
import server.handlers.auth_handler as auth_handler
import server.handlers.matchmaking_handler as matchmaking_handler
import server.handlers.room_handler as room_handler
import server.handlers.placement_handler as placement_handler
import server.handlers.game_handler as game_handler
import server.handlers.replay_handler as replay_handler
import server.handlers.leaderboard_handler as leaderboard_handler
from shared.message_type import (
    LOGIN,
    REGISTER,
    ROOM_WAITING_CREATED,
    PING,
    PONG,
    MATCHMAKE,
    CREATE_ROOM,
    GET_ROOM_LIST,
    JOIN_ROOM,
    LEAVE_ROOM,
    START_PLACEMENT,
    PLACE_SHIPS,
    READY,
    FIRE,
    FORFEIT,
    JOIN_SPECTATOR,
    GET_LEADERBOARD,
    GET_REPLAY_LIST,
    GET_REPLAY_DETAIL,
    REMATCH_REQUEST,
    ERROR
)


class ClientHandler:
    active_usernames = {}
    active_lock = threading.Lock()

    def __init__(self, client_socket, address, logger, matchmaking):
        self.client_socket = client_socket
        self.address = address
        self.logger = logger
        self.matchmaking = matchmaking

        self.buffer = ""
        self.username = None
        self.session_id = None
        self.room_id = None

    def handle(self):
        self.client_socket.settimeout(300)

        try:
            while True:
                data = self.client_socket.recv(4096)

                if not data:
                    self.logger.info(f"Client disconnected: {self.address}")
                    break

                self.buffer += data.decode("utf-8")

                while "\n" in self.buffer:
                    raw_message, self.buffer = self.buffer.split("\n", 1)
                    self.process_message(raw_message)

        except ConnectionResetError:
            self.logger.warning(f"Connection reset: {self.address}")

        except socket.timeout:
            self.logger.warning(f"Client timeout: {self.address}")

        finally:
            if self.room_id:
                room_handler.handle_leave_room(self)

            auth_handler.unregister_active_user(self)
            self.client_socket.close()

    def process_message(self, raw_message):
        try:
            message = decode_message(raw_message)
        except json.JSONDecodeError:
            self.send_error("Malformed JSON packet")
            return

        message_type = message.get("type")

        if message_type == LOGIN:
            auth_handler.handle_login(self, message)
        elif message_type == REGISTER:
            auth_handler.handle_register(self, message)
        elif message_type == PING:
            self.handle_ping(message)
        elif message_type == MATCHMAKE:
            matchmaking_handler.handle_matchmake(self)
        elif message_type == CREATE_ROOM:
            room_handler.handle_create_room(self, message)
        elif message_type == GET_ROOM_LIST:
            room_handler.handle_get_room_list(self)
        elif message_type == JOIN_ROOM:
            room_handler.handle_join_room(self, message)
        elif message_type == LEAVE_ROOM:
            room_handler.handle_leave_room(self)
        elif message_type == START_PLACEMENT:
            placement_handler.handle_start_placement(self)
        elif message_type == PLACE_SHIPS:
            placement_handler.handle_place_ships(self, message)
        elif message_type == READY:
            placement_handler.handle_ready(self, message)
        elif message_type == FIRE:
            game_handler.handle_fire(self, message)
        elif message_type == FORFEIT:
            game_handler.handle_forfeit(self)
        elif message_type == GET_LEADERBOARD:
            leaderboard_handler.handle_get_leaderboard(self)
        elif message_type == GET_REPLAY_LIST:
            replay_handler.handle_get_replay_list(self)
        elif message_type == GET_REPLAY_DETAIL:
            replay_handler.handle_get_replay_detail(self, message)
        elif message_type == REMATCH_REQUEST:
            self.handle_rematch_request()
        else:
            self.send_error(f"Unknown message type: {message_type}")

    def handle_rematch_request(self):
        if not self.room_id:
            self.send_error("You are not in a room")
            return

        room = self.matchmaking.room_manager.get_room(self.room_id)

        if not room:
            self.send_error("Room not found")
            return

        if room.status in ["IN_GAME", "WAITING_PLACEMENT"]:
            self.send_error("Cannot rematch before game over")
            return

        existing_player = room.get_player(self.session_id)

        if existing_player is None and room.status == "WAITING_OPPONENT" and len(room.players) == 1:
            player = {
                "username": self.username,
                "session_id": self.session_id,
                "handler": self
            }

            success, info = room.add_player(player)

            if not success:
                self.send_error(info)
                return

            self.room_id = room.room_id
            room_handler.notify_match_found(self, room)
            return

        success, info = room.reset_for_rematch_request(self.session_id)

        if not success:
            self.send_error(info)
            return

        self.room_id = room.room_id

        from shared.message_type import REMATCH_WAITING

        self.send({
            "type": REMATCH_WAITING,
            "status": "OK",
            "room_id": room.room_id,
            "payload": {
                "room": room.get_public_info(),
                "message": info
            }
        })

        room_handler.notify_room_updated(self, room)

        self.logger.info(f"{self.username} requested rematch in room {room.room_id}")

    def handle_ping(self, message):
        self.send(ok(PONG, message.get("payload", {})))

    def send_error(self, error_message):
        self.logger.warning(f"Error sent to {self.address}: {error_message}")
        self.send(error(error_message))

    def send(self, message):
        try:
            self.client_socket.sendall(encode_message(message))
        except OSError as send_error:
            self.logger.warning(f"Failed to send to {self.address}: {send_error}")
