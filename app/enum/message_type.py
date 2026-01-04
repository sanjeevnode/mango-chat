from enum import Enum

class MessageType(Enum):
    INFO: str = "info"
    text: str = "text"
    reply: str = "reply"