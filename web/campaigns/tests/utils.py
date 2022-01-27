"""Contains utilities to help with writing tests."""

import typing as _t
from campaigns import models as campaign_models


def get_campaign(
    id: int = 1,
    structure_value: str = "test_structure_value",
    status: str = "test_status",
) -> campaign_models.Campaign:
    """Creates (if needed) and returns a `Campaign` instance.

    Args:
        id: The id of the `Campaign` instance.
        structure_value: The value of the `structure_value` field.
        status: The value of the `status` field.

    Returns:
        The `Campaign` instance.
    """
    return campaign_models.Campaign.objects.get_or_create(
        id=id,
        structure_value=structure_value,
        status=status,
    )[0]


def get_ad_group(
    id: int = 1,
    campaign: _t.Optional[campaign_models.Campaign] = None,
    alias: str = "test_alias",
    status: str = "test_status",
) -> campaign_models.AdGroup:
    """Creates (if needed) and returns an `AdGroup` instance.

    Args:
        id: The id of the `AdGroup` instance.
        campaign: The `Campaign` instance.
        alias: The value of the `alias` field.
        status: The value of the `status` field.

    Returns:
        The `AdGroup` instance.
    """
    return campaign_models.AdGroup.objects.get_or_create(
        id=id,
        campaign=campaign or get_campaign(id),
        alias=alias,
        status=status,
    )[0]
