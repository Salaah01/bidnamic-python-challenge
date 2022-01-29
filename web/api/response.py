"""Module contains wrappers for an API response. The wrappers are designed to
be conform to a predetermined format.
"""
import typing as _t
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from . import utils


def base_response(
    request: Request,
    metadata: _t.Optional[dict] = None,
    data: _t.Optional[_t.Any] = None,
) -> dict:
    """Responsible for arranging the response in a specific format. This is
    essentially a wrapper to ensure that the response is in the correct format
    for the API.

    Args:
        request: The request object.
        metadata: A dictionary of metadata to be included in the response.
        data: The data to be returned to the user.

    Returns:
        A dictionary containing the response.
    """
    return {
        "metadata": utils.build_metadata(request, metadata),
        "data": data or {},
    }


def success(
    request: Request,
    data: _t.Optional[_t.Any] = None,
    metadata: _t.Optional[dict] = None,
    status: _t.Optional[int] = status.HTTP_200_OK,
) -> Response:
    """A wrapper for returning an API response after a successful request.

    Args:
        data: The data to be returned to the user.
        metadata: Additional metadata to include in the response.
        status: The status code to return.

    Returns:
        A response object.
    """
    return Response(base_response(request, metadata, data), status=status)
