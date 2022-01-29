"""Unittests for the models."""

from django.test import TransactionTestCase
import pandas as pd
from .. import models as campaign_models
from .utils import get_campaign, get_ad_group


class TestCampaign(TransactionTestCase):
    """Unittests for the `Campaign` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_campaign()), str)

    def test_load_from_dataframe(self):
        """Test that the method is able to successfully bulk, insert or update
        records into the database.
        """

        # Add a campaign to the database where the record id also appears in
        # the dataset. This will allow us test that the record is updated.
        campaign_models.Campaign.objects.create(
            id=50,
            structure_value="b",
            status="c",
        )

        df = pd.DataFrame(
            {
                "campaign_id": [50, 100, 50],
                "structure_value": ["a", "a", "a"],
                "status": ["ENABLED", "ENABLED", "DISABLED"],
            }
        )

        campaign_models.Campaign.load_from_dataframe(df)
        campaigns = campaign_models.Campaign.objects.all()

        self.assertEqual(campaigns.count(), 2)
        campaign_50 = campaigns.filter(id=50).first()
        if campaign_50 is None:
            self.fail("Campaign 1 not found.")
        self.assertEqual(campaign_50.structure_value, "a")
        self.assertEqual(campaign_50.status, "DISABLED")

        campaign_100 = campaigns.filter(id=100).first()
        if campaign_100 is None:
            self.fail("Campaign 2 not found.")
        self.assertEqual(campaign_100.structure_value, "a")
        self.assertEqual(campaign_100.status, "ENABLED")


class TestAdGroup(TransactionTestCase):
    """Unittests for the `AdGroup` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_ad_group()), str)

    def test_load_from_dataframe(self):
        """Test that the method successfully loads data into the table."""

        # AdGroups depends on Campaigns, so we need to create a set of
        # campaigns first.
        for i in (50, 100, 150):
            campaign_models.Campaign.objects.create(
                id=i,
                structure_value=i,
                status=i,
            ).save()

        # Add an ad group where the record id also appears in the dataset.
        # This will allow us test that the record is updated.
        campaign_models.AdGroup.objects.create(
            id=50, campaign_id=50, alias="old_alias", status="old_status"
        ).save()

        df = pd.DataFrame(
            {
                "ad_group_id": [50, 100, 50, 99],
                "campaign_id": [50, 100, 50, 99],
                "alias": ["a", "b", "c", "99"],
                "status": ["ENABLED", "ENABLED", "DISABLED", "a"],
            }
        )

        campaign_models.AdGroup.load_from_dataframe(df)
        ad_groups = campaign_models.AdGroup.objects.all()

        self.assertEqual(ad_groups.count(), 2, ad_groups.all())
        ad_group_50 = ad_groups.filter(id=50).first()
        if ad_group_50 is None:
            self.fail("AdGroup 1 not found.")
        self.assertEqual(ad_group_50.campaign_id, 50)
        self.assertEqual(ad_group_50.alias, "c")
        self.assertEqual(ad_group_50.status, "DISABLED")

        ad_group_100 = ad_groups.filter(id=100).first()
        if ad_group_100 is None:
            self.fail("AdGroup 2 not found.")
        self.assertEqual(ad_group_100.campaign_id, 100)
        self.assertEqual(ad_group_100.alias, "b")
        self.assertEqual(ad_group_100.status, "ENABLED")
