import socket
import threading

from shared.serializer import encode_message, decode_message


class NetworkClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = ""
        self.connected = False
        self.on_message = None

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.connected = True

        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        while self.connected:
            try:
                data = self.socket.recv(4096)

                if not data:
                    self.connected = False
                    break

                self.buffer += data.decode("utf-8")

                while "\n" in self.buffer:
                    raw_message, self.buffer = self.buffer.split("\n", 1)
                    message = decode_message(raw_message)

                    if self.on_message:
                        self.on_message(message)

            except OSError:
                self.connected = False
                break

    def send(self, message):
        self.socket.sendall(encode_message(message))

    def close(self):
        self.connected = False
        self.socket.close()
