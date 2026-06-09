import socket
import json


HOST = "127.0.0.1"
PORT = 5000


def send_raw(sock, raw):
    sock.sendall(raw.encode("utf-8"))


def receive(sock):
    buffer = ""

    while "\n" not in buffer:
        data = sock.recv(4096)
        if not data:
            return None
        buffer += data.decode("utf-8")

    raw_message, _ = buffer.split("\n", 1)
    return json.loads(raw_message)


def test_malformed_json():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    send_raw(sock, "{bad json}\n")
    response = receive(sock)

    print("Malformed JSON test:", response)
    sock.close()


def test_unknown_message_type():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    send_raw(sock, json.dumps({
        "type": "HACK_SERVER",
        "payload": {}
    }) + "\n")

    response = receive(sock)

    print("Unknown message type test:", response)
    sock.close()


def test_matchmake_without_login():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    send_raw(sock, json.dumps({
        "type": "MATCHMAKE",
        "payload": {}
    }) + "\n")

    response = receive(sock)

    print("Matchmake without login test:", response)
    sock.close()


if __name__ == "__main__":
    test_malformed_json()
    test_unknown_message_type()
    test_matchmake_without_login()