from dataclasses import dataclass


@dataclass
class PagingRS:
    page: int
    size: int
    total_page: int
    totals: int

    @classmethod
    def from_page(cls, page_obj):
        return cls(
            page=page_obj.number,
            size=page_obj.paginator.per_page,
            total_page=page_obj.paginator.num_pages,
            totals=page_obj.paginator.count,
        )
