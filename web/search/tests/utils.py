"""Contains utilities to help with writing tests."""

import typing as _t
from datetime import date as _date
from campaigns import models as campaign_models
from campaigns.tests import utils as campaign_test_utils
from search import models as search_models


def get_search_term(
    date: _date = _date(2022, 1, 1),
    ad_group: _t.Optional[campaign_models.AdGroup] = None,
    clicks: int = 1,
    cost: float = 1.0,
    conversion_value: float = 1.0,
    conversions: int = 1,
    search_term: str = "test_search_term",
) -> search_models.SearchTerm:
    """Creates (if needed) and returns a `SearchTerm` instance.

    Args:
        date: The search date
        ad_group: The `AdGroup` instance.
        clicks: The value of the `clicks` field.
        cost: The value of the `cost` field.
        conversion_value: The value of the `conversion_value` field.
        conversions: The value of the `conversions` field.
        search_term: The value of the `search_term` field.

    Returns:
        The `SearchTerm` instance.
    """
    return search_models.SearchTerm.objects.get_or_create(
        date=date,
        ad_group=ad_group or campaign_test_utils.get_ad_group(),
        clicks=clicks,
        cost=cost,
        conversion_value=conversion_value,
        conversions=conversions,
        search_term=search_term,
    )[0]
