import json


def encode_message(message: dict) -> bytes:
    """
    Encode dictionary menjadi JSON bytes dengan newline delimiter.
    Newline delimiter dipakai supaya receiver tahu batas akhir 1 message.
    """
    return (json.dumps(message) + "\n").encode("utf-8")


def decode_message(raw_message: str) -> dict:
    """
    Decode string JSON menjadi dictionary.
    """
    return json.loads(raw_message)