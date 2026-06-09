import uuid

from server.auth_service import register_user, login_user
from server.response_builder import ok, failed
from shared.message_type import (
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    REGISTER_SUCCESS,
    REGISTER_FAILED
)


def handle_login(handler, message):
    username = message.get("payload", {}).get("username", "").strip()
    password = message.get("payload", {}).get("password", "")

    success, info = login_user(username, password)

    if not success:
        handler.send(failed(LOGIN_FAILED, info))
        return

    with handler.__class__.active_lock:
        active_handler = handler.__class__.active_usernames.get(username)

        if active_handler is not None and active_handler is not handler:
            handler.send(failed(LOGIN_FAILED, "Username sedang online"))
            return

        handler.username = username
        handler.session_id = str(uuid.uuid4())
        handler.__class__.active_usernames[handler.username] = handler

    handler.logger.info(f"User logged in: {handler.username} from {handler.address}")

    handler.send(ok(
        LOGIN_SUCCESS,
        session_id=handler.session_id,
        payload={
            "username": handler.username,
            "message": info
        }
    ))


def unregister_active_user(handler):
    if not handler.username:
        return

    with handler.__class__.active_lock:
        active_handler = handler.__class__.active_usernames.get(handler.username)

        if active_handler is handler:
            del handler.__class__.active_usernames[handler.username]


def handle_register(handler, message):
    username = message.get("payload", {}).get("username", "")
    password = message.get("payload", {}).get("password", "")

    success, info = register_user(username, password)

    if not success:
        handler.send(failed(REGISTER_FAILED, info))
        return

    handler.send(ok(
        REGISTER_SUCCESS,
        payload={
            "username": username.strip(),
            "message": info
        }
    ))

    handler.logger.info(f"User registered: {username.strip()}")
