from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from ..base import BaseController, StructureRS
from ..exception import CategoryException
from ..base import Metadata, metadata_handler
from ..serializers import (
    CategoryCreateSerializer,
    CategoryListSerializer,
    CategoryResponseSerializer,
    CategoryUpdateSerializer,
)
from ..services import CategoryService


class CategoryViewSet(BaseController, ViewSet):
    category_service = CategoryService()

    @metadata_handler(required_user_id=True)
    def list(self, request: Request, *, metadata: Metadata):
        try:
            categories = self.category_service.list(metadata.user_id)
            data = CategoryListSerializer(categories, many=True).data
            structure = StructureRS.with_status_message_data(
                status.HTTP_200_OK, "Categories retrieved", data
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @metadata_handler(required_user_id=True)
    def retrieve(self, request: Request, pk: int = None, *, metadata: Metadata):
        try:
            category = self.category_service.detail(int(pk), metadata.user_id)
            data = CategoryResponseSerializer(category).data
            structure = StructureRS.with_status_message_data(
                status.HTTP_200_OK, "Category retrieved", data
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @metadata_handler(required_user_id=True)
    def create(self, request: Request, *, metadata: Metadata):
        try:
            serializer = CategoryCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            saved_category = self.category_service.create(
                serializer.validated_data, metadata
            )
            structure = StructureRS.with_status_message_data(
                status.HTTP_201_CREATED,
                "Category created",
                CategoryResponseSerializer(saved_category).data,
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @metadata_handler(required_user_id=True)
    def update(self, request: Request, pk: int = None, *, metadata: Metadata):
        try:
            serializer = CategoryUpdateSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_category = self.category_service.update(
                int(pk),
                serializer.validated_data,
                metadata,
                set_fields=set(serializer.validated_data.keys()),
            )
            structure = StructureRS.with_status_message_data(
                status.HTTP_200_OK,
                "Category updated",
                CategoryResponseSerializer(updated_category).data,
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @metadata_handler(required_user_id=True)
    def destroy(self, request: Request, pk: int = None, *, metadata: Metadata):
        try:
            self.category_service.delete(int(pk), metadata)
            structure = StructureRS.with_message(
                status.HTTP_200_OK, "Category deleted"
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @action(detail=True, methods=["post"])
    @metadata_handler(required_user_id=True)
    def enable(self, request: Request, pk: int = None, *, metadata: Metadata):
        try:
            category = self.category_service.enable(int(pk), metadata)
            structure = StructureRS.with_status_message_data(
                status.HTTP_200_OK,
                "Category enabled",
                CategoryResponseSerializer(category).data,
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)

    @action(detail=True, methods=["post"])
    @metadata_handler(required_user_id=True)
    def disable(self, request: Request, pk: int = None, *, metadata: Metadata):
        try:
            category = self.category_service.disable(int(pk), metadata)
            structure = StructureRS.with_status_message_data(
                status.HTTP_200_OK,
                "Category disabled",
                CategoryResponseSerializer(category).data,
            )
            return self.response(structure)
        except CategoryException as exc:
            return self.response_error(message=exc.message, status_code=exc.status_code)
