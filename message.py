import json

class Message:
    @staticmethod
    def encode(message: dict) -> bytes:
        return json.dumps(message).encode()
    @staticmethod
    def decode(message: bytes) -> dict:
        return json.loads(message.decode())