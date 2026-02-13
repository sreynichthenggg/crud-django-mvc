from dataclasses import dataclass

from .constants import SUCCESSFULLY


@dataclass
class StructureRS:
    status: int = 200
    message: str = SUCCESSFULLY
    message_key: str = SUCCESSFULLY.lower()
    data: object | None = None
    paging: object | None = None

    def __post_init__(self):
        if not self.message_key and self.message:
            self.message_key = self.message.replace(" ", "_").lower()

    @classmethod
    def with_message(cls, status: int, message: str):
        return cls(status=status, message=message, message_key=message.replace(" ", "_").lower())

    @classmethod
    def with_data(cls, data, paging=None):
        return cls(data=data, paging=paging)

    @classmethod
    def with_status_message_data(cls, status: int, message: str, data):
        return cls(
            status=status,
            message=message,
            message_key=message.replace(" ", "_").lower(),
            data=data,
        )
