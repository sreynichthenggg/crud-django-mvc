from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework import status

from ..base import BaseListingRQ, BaseService, PagingRS
from ..exception import CategoryException
from ..base import Metadata
from ..serializers import CategoryListSerializer, CategoryResponseSerializer
from ..repositories import CategoryRepository


class CategoryService(BaseService):
    def __init__(self):
        self.repo = CategoryRepository()

    def list(self, user_id: str):
        if not user_id:
            raise CategoryException("user_id is required")
        return self.repo.list_by_user(user_id)

    def get_all_category_admin(self, listing: BaseListingRQ):
        qs = self.repo.list_all()
        if listing.has_query() and listing.get_query() != "ALL":
            qs = qs.filter(name__icontains=listing.get_query())

        qs = qs.order_by(listing.get_ordering())
        paginator = Paginator(qs, listing.get_size())
        page_obj = paginator.get_page(listing.get_page())

        data = [CategoryListSerializer(category).data for category in page_obj.object_list]
        paging = PagingRS.from_page(page_obj)
        return self.response_data_paging(data, paging)

    def get_category_by_id(self, pk: int):
        category = self.repo.get_by_id(pk)
        if not category:
            return self.response_status(status.HTTP_404_NOT_FOUND, "Category not found")
        return self.response_data(CategoryResponseSerializer(category).data)

    def detail(self, pk: int, user_id: str):
        if not user_id:
            raise CategoryException("user_id is required")
        category = self.repo.get_by_id_user(pk, user_id)
        if not category:
            raise CategoryException("Category not found", status_code=404)
        return category

    def create(self, data: dict, metadata: Metadata):
        if self.repo.exists_by_name_user(data.get("name", ""), metadata.user_id):
            raise CategoryException("name already exists")
        parent = self._get_parent(data.get("parent_id"), metadata.user_id)
        return self.repo.create(
            name=data.get("name", ""),
            icon=data.get("icon", ""),
            user_id=metadata.user_id,
            parent=parent,
            status=True if data.get("status") is None else data.get("status"),
            created_by=data.get("created_by") or metadata.user_id,
        )

    def update(
        self,
        pk: int,
        data: dict,
        metadata: Metadata,
        *,
        set_fields: set[str],
    ):
        category = self.detail(pk, metadata.user_id)

        if "name" in set_fields:
            if not data.get("name"):
                raise CategoryException("name is required")
            if self.repo.exists_by_name_user(
                data.get("name", ""), metadata.user_id, exclude_id=pk
            ):
                raise CategoryException("name already exists")
            category.name = data.get("name", "")
        if "icon" in set_fields:
            category.icon = data.get("icon", "")
        if "parent_id" in set_fields:
            category.parent = self._get_parent(data.get("parent_id"), metadata.user_id)
        if "status" in set_fields:
            category.status = data.get("status")
        category.updated_by = metadata.user_id

        category.updated_at = timezone.now()
        return self.repo.save(category)


    def delete(self, pk: int, metadata: Metadata):
        category = self.detail(pk, metadata.user_id)
        self.repo.delete(category)

    def enable(self, pk: int, metadata: Metadata):
        category = self.detail(pk, metadata.user_id)
        category.status = True
        category.updated_at = timezone.now()
        category.updated_by = metadata.user_id
        return self.repo.save(category)

    def disable(self, pk: int, metadata: Metadata):
        category = self.detail(pk, metadata.user_id)
        category.status = False
        category.updated_at = timezone.now()
        category.updated_by = metadata.user_id
        return self.repo.save(category)

    def _get_parent(self, parent_id: int | None, user_id: str | None):
        if parent_id is None:
            return None
        parent = self.repo.get_parent(parent_id, user_id)
        if not parent:
            raise CategoryException("parent_id not found", status_code=404)
        return parent
