from dataclasses import dataclass


@dataclass
class BaseListingRQ:
    page: int | None = None
    size: int | None = None
    query: str | None = None
    sort: str | None = None
    order: str | None = None

    def get_size(self) -> int:
        return 20 if self.size is None else self.size

    def get_sort(self) -> str:
        return "id" if not self.sort else self.sort

    def get_order(self) -> str:
        if not self.order:
            return "DESC"
        normalized = self.order.upper()
        return normalized if normalized in {"ASC", "DESC"} else "DESC"

    def get_page(self) -> int:
        if not self.page or self.page <= 0:
            return 1
        return self.page

    def has_query(self) -> bool:
        return bool(self.query)

    def get_query(self) -> str:
        return self.query or "ALL"

    def get_ordering(self) -> str:
        prefix = "-" if self.get_order() == "DESC" else ""
        return f"{prefix}{self.get_sort()}"
