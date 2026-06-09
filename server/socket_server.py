import socket
import threading

from server.config import HOST, PORT
from server.client_handler import ClientHandler
from server.logger import setup_logger
from server.room_manager import RoomManager
from server.matchmaking import Matchmaking
from server.database import init_database


class SocketServer:
    def __init__(self):
        init_database()

        self.logger = setup_logger()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.room_manager = RoomManager()
        self.matchmaking = Matchmaking(self.room_manager)

    

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()

        self.logger.info(f"Server started on {HOST}:{PORT}")
        print(f"[SERVER] Running on {HOST}:{PORT}")

        while True:
            client_socket, address = self.server_socket.accept()
            self.logger.info(f"Client connected from {address}")
            print(f"[SERVER] Client connected from {address}")

            handler = ClientHandler(
                client_socket=client_socket,
                address=address,
                logger=self.logger,
                matchmaking=self.matchmaking
            )

            thread = threading.Thread(target=handler.handle, daemon=True)
            thread.start()