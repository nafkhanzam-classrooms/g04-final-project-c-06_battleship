import socket
import json
import time
import threading
import uuid


HOST = "127.0.0.1"
PORT = 5000
TOTAL_CLIENTS = 50


def send_message(sock, message):
    raw = json.dumps(message) + "\n"
    sock.sendall(raw.encode("utf-8"))


def receive_message(sock):
    buffer = ""

    while "\n" not in buffer:
        data = sock.recv(4096)
        if not data:
            return None
        buffer += data.decode("utf-8")

    raw_message, _ = buffer.split("\n", 1)
    return json.loads(raw_message)


def dummy_client(index):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_time = time.time()
        sock.connect((HOST, PORT))
        connect_time = time.time() - start_time

        username = f"dummy_{index}_{uuid.uuid4().hex[:4]}"

        send_message(sock, {
            "type": "LOGIN",
            "payload": {
                "username": username
            }
        })

        login_response = receive_message(sock)

        send_message(sock, {
            "type": "PING",
            "session_id": login_response.get("session_id") if login_response else None,
            "payload": {
                "sent_at": time.time()
            }
        })

        ping_response = receive_message(sock)

        if ping_response and ping_response["type"] == "PONG":
            latency = (time.time() - ping_response["payload"]["sent_at"]) * 1000
        else:
            latency = None

        print(
            f"[CLIENT {index}] connected={round(connect_time * 1000, 2)}ms "
            f"ping={round(latency, 2) if latency else 'failed'}ms"
        )

        sock.close()

    except Exception as error:
        print(f"[CLIENT {index}] ERROR: {error}")


def main():
    threads = []
    start = time.time()

    for i in range(TOTAL_CLIENTS):
        thread = threading.Thread(target=dummy_client, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    duration = time.time() - start
    print(f"\nLoad test finished: {TOTAL_CLIENTS} clients in {round(duration, 2)}s")


if __name__ == "__main__":
    main()