from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from ..base import BaseController, BaseListingRQ
from ..exception import CategoryException
from ..services import CategoryService


def _to_int(value):
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


class AdminCategoryViewSet(BaseController, ViewSet):
    category_service = CategoryService()

    def list(self, request: Request):
        try:
            listing = BaseListingRQ(
                page=_to_int(request.query_params.get("page")),
                size=_to_int(request.query_params.get("size")),
                query=request.query_params.get("query"),
                sort=request.query_params.get("sort"),
                order=request.query_params.get("order"),
            )
            structure = self.category_service.get_all_category_admin(listing)
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    def retrieve(self, request: Request, pk: int = None):
        try:
            structure = self.category_service.get_category_by_id(int(pk))
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)
