"""Search Views."""

import typing as _t
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api import response as api_response, exceptions as api_exceptions
from . import models as search_models, serializers


def apply_limit(
    request: Request,
    queryset: QuerySet[search_models.SearchTerm],
    default_limit: int = 10,
) -> QuerySet[search_models.SearchTerm]:
    """Applies a limit to a queryset.

    Args:
        request - The request object.
        queryset - The queryset to apply the limit to.
        default_limit - The default limit to apply if none is provided.

    Returns:
        The queryset with the limit applied.
    """
    limit = request.GET.get("limit") or request.data.get("limit")
    if limit == "all":
        return queryset
    if limit is None:
        limit = default_limit

    if not str(limit).isdigit():
        raise api_exceptions.ValidationError(
            request, error="`limit` must be an integer or `all`."
        )

    return queryset[: int(limit)]


@api_view(["GET"])
def roas_by_structured_value(
    request: Request, structured_value: _t.Optional[str] = None
) -> Response:
    """API view for retriving RoAS by a campaign's structured by ordered by
    RoAS (desc).

    Args:
        request - The request object.
        structured_value - The structured value to search for.
    """

    if structured_value is None:
        structured_value = request.data.get("structured_value")

    if structured_value is None:
        raise api_exceptions.ValidationError(
            request, error="`structured_value` is required."
        )

    searches = search_models.SearchTerm.for_structure_value(
        structured_value
    ).order_by("-roas")

    searches = apply_limit(request, searches)

    return api_response.success(
        request, serializers.SearchTermSerializer(searches, many=True).data
    )


@api_view(["GET"])
def roas_by_alias(
    request: Request, alias: _t.Optional[str] = None
) -> Response:
    """API view for retriving RoAS by an ad group's alias.

    Args:
        request - The request object.
        alias - The alias to search for.
    """

    if alias is None:
        alias = request.data.get("alias")

    if alias is None:
        raise api_exceptions.ValidationError(
            request, error="`alias` is required."
        )

    searches = search_models.SearchTerm.for_alias(alias).order_by("-roas")

    searches = apply_limit(request, searches)

    return api_response.success(
        request, serializers.SearchTermSerializer(searches, many=True).data
    )
