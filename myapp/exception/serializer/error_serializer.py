from dataclasses import dataclass


@dataclass
class ErrorSerializer:
    status: int
    message: str
    errors: object | None = None

    def to_dict(self) -> dict[str, object]:
        payload = {"status": self.status, "message": self.message}
        if self.errors is not None:
            payload["errors"] = self.errors
        return payload
