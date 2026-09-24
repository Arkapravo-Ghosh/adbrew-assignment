import logging

from pymongo.errors import ConnectionFailure
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from .exceptions import InvalidInputError

logger = logging.getLogger(__name__)


def _error_response(message: str, status_code: int) -> Response:
    return Response({"error": message}, status=status_code)


def api_exception_handler(exc, context):
    if isinstance(exc, InvalidInputError):
        return _error_response(str(exc), status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ConnectionFailure):
        logger.error("Database unreachable: %s", exc, exc_info=exc)
        return _error_response(
            "Service temporarily unavailable. Please try again later.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Let DRF handle its own exceptions (malformed JSON, wrong HTTP method, ...),
    # then reshape them to match our {"error": ...} format.
    response = drf_exception_handler(exc, context)
    if response is not None and "detail" in response.data:
        response.data = {"error": response.data["detail"]}
    return response
