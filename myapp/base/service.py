from rest_framework import status

from .paging import PagingRS
from .structure import StructureRS


class BaseService:
    def response(self):
        return StructureRS()

    def response_data(self, data):
        return StructureRS.with_data(data)

    def response_data_paging(self, data, paging: PagingRS):
        return StructureRS.with_data(data, paging)

    def response_status(self, http_status: int, message: str):
        return StructureRS.with_message(http_status, message)

    def response_status_data(self, http_status: int, message: str, data):
        return StructureRS.with_status_message_data(http_status, message, data)

    def response_created(self, message: str, data=None):
        return StructureRS.with_status_message_data(
            status.HTTP_201_CREATED, message, data
        )
