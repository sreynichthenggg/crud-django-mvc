import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from ..base.structure import StructureRS
from .category_exception import CategoryException
from .message import Message


class ExceptionAdvices:
    @staticmethod
    def handle(exc, context):
        if isinstance(exc, CategoryException):
            structure = StructureRS.with_message(exc.status_code, exc.message)
            payload = structure.__dict__
            if exc.errors is not None:
                payload["errors"] = exc.errors
            return Response(payload, status=structure.status)

        response = drf_exception_handler(exc, context)
        if response is not None:
            structure = StructureRS.with_message(response.status_code, Message.BAD_REQUEST)
            payload = structure.__dict__
            payload["errors"] = response.data
            if settings.DEBUG:
                payload["detail"] = str(exc)
                payload["trace"] = traceback.format_exc()
            return Response(payload, status=response.status_code)

        structure = StructureRS.with_message(
            status.HTTP_500_INTERNAL_SERVER_ERROR, Message.INTERNAL_SERVER_ERROR
        )
        payload = structure.__dict__
        if settings.DEBUG:
            payload["detail"] = str(exc)
            payload["trace"] = traceback.format_exc()
        return Response(payload, status=structure.status)


def exception_handler(exc, context):
    return ExceptionAdvices.handle(exc, context)
