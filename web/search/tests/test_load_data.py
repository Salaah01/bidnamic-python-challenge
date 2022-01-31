"""Integration for commands to load data into the database."""

import os
from django.test import TransactionTestCase
from django.conf import settings
from django.core.management import call_command
from search import models as search_models
from campaigns.tests.utils import get_ad_group


class TestLoadData(TransactionTestCase):
    """Integration tests for commands to load data into the database."""

    testcases_dir = test_filepath = os.path.join(
        settings.BASE_DIR,
        "search",
        "tests",
    )

    def test_search_terms(self):
        """Test the `search_terms` command."""

        get_ad_group(10)
        get_ad_group(20)

        call_command(
            "load_search_terms",
            "-f",
            os.path.join(
                self.testcases_dir, "load_data_search_terms_testcases.csv"
            ),
        )
        self.assertEqual(search_models.SearchTerm.objects.count(), 2)
