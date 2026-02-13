from rest_framework import status
from rest_framework.response import Response

from .constants import SUCCESSFULLY
from .paging import PagingRS
from .structure import StructureRS


class BaseController:
    def response(self, structure: StructureRS | None = None):
        if structure is None:
            structure = StructureRS(status=status.HTTP_200_OK, message=SUCCESSFULLY)
        return Response(structure.__dict__, status=structure.status)

    def response_data(self, data):
        structure = StructureRS.with_data(data)
        return Response(structure.__dict__, status=structure.status)

    def response_data_paging(self, data, paging: PagingRS):
        structure = StructureRS.with_data(data, paging)
        return Response(structure.__dict__, status=structure.status)

    def response_error(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        structure = StructureRS.with_message(status_code, message)
        return Response(structure.__dict__, status=structure.status)
