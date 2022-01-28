"""Module contains custom exceptions for the APIs. The exception responses are
designed to be consistent with the API response format.
"""

import typing as _t
from rest_framework import exceptions
from rest_framework.request import Request
from .response import base_response


def base_exception(
    request: Request,
    metadata: _t.Optional[dict] = None,
    data: _t.Optional[_t.Any] = None,
    error: _t.Optional[str] = None,
) -> dict:
    """Responsible for arranging the response in a specific format. This is
    essentially a wrapper to ensure that the response is in the correct format
    for the API where the response needs to indicate some form of error.

    Args:
        request: The request object.
        metadata: A dictionary of metadata to be included in the response.
        data: The data to be returned to the user.
        error: The error to be returned to the user.

    Returns:
        A dictionary containing the response.
    """
    res = base_response(
        request=request,
        metadata=metadata,
        data=data,
    )
    res.update({"error": error})
    return res


class ValidationError(exceptions.ValidationError):
    def __init__(
        self,
        request: Request,
        metadata: _t.Optional[dict] = None,
        data: _t.Optional[_t.Any] = None,
        error: _t.Optional[str] = None,
        code=None,
    ):
        """Custom exception for validation errors. Extends the DRF standard
        validation error.

        Args:
            request: The request object.
            metadata: A dictionary of metadata to be included in the response.
            data: The data to be returned to the user.
            error: The error to be returned to the user.
            code: The error code to return.
        """
        super().__init__(
            base_exception(
                request=request,
                metadata=metadata,
                data=data,
                error=error,
            ),
            code,
        )


class NotFoundError(exceptions.NotFound):
    def __init__(
        self,
        request: Request,
        metadata: _t.Optional[dict] = None,
        data: _t.Optional[_t.Any] = None,
        error: _t.Optional[str] = None,
        code=None,
    ):
        """Custom exception for not found errors. Extends the DRF standard
        not found error.

        Args:
            request: The request object.
            metadata: A dictionary of metadata to be included in the response.
            data: The data to be returned to the user.
            error: The error to be returned to the user.
            code: The error code to return.
        """
        super().__init__(
            base_exception(
                request=request,
                metadata=metadata,
                data=data,
                error=error,
            ),
            code,
        )
