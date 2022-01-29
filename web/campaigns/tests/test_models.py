"""Unittests for the models."""

from django.test import TestCase
import pandas as pd
from .. import models as campaign_models
from .utils import get_campaign, get_ad_group


class TestCampaign(TestCase):
    """Unittests for the `Campaign` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_campaign()), str)

    def test_load_from_dataset(self):
        """Test that the method is able to successfully bulk, insert or update
        records into the database.
        """

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

        campaign_models.Campaign.load_from_dataset(df)
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


class TestAdGroup(TestCase):
    """Unittests for the `AdGroup` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_ad_group()), str)
