import typing as _t
from rest_framework.request import Request


def build_metadata(
    request: Request,
    metadata: _t.Optional[dict] = None,
) -> _t.Dict[str, _t.Any]:
    """Helper function to generate the metadata for a response. As a minimum,
    the request object should be provided so that the system is able to get
    query paramers.

    Args:
        request: The request object.
        metadata: Any other metadata to be included in the response.

    Returns:
        A dictionary containing the metadata.
    """

    return {
        # We do not return the value for the post as it may contain sensitive
        # information.
        "query_params": request.GET.dict(),
        **(metadata or {}),
    }
