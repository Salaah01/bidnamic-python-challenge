"""Integration for commands to load data into the database."""

import os
from django.test import TransactionTestCase
from django.conf import settings
from django.core.management import call_command
from campaigns import models as campaign_models
from .utils import get_campaign


class TestLoadData(TransactionTestCase):
    """Integration tests for commands to load data into the database."""

    testcases_dir = test_filepath = os.path.join(
        settings.BASE_DIR,
        "campaigns",
        "tests",
    )

    def test_load_campaigns(self):
        """Test the `load_campaigns` command."""
        call_command(
            "load_campaigns",
            "-f",
            os.path.join(
                self.testcases_dir, "load_data_campaigns_testcases.csv"
            ),
        )
        self.assertEqual(campaign_models.Campaign.objects.count(), 2)

    def test_load_ad_groups(self):
        """Test the `load_ad_groups` command."""

        # Load campaigns
        get_campaign(10)
        get_campaign(20)

        call_command(
            "load_ad_groups",
            "-f",
            os.path.join(
                self.testcases_dir, "load_data_ad_groups_testcases.csv"
            ),
        )

        self.assertEqual(campaign_models.AdGroup.objects.count(), 2)
