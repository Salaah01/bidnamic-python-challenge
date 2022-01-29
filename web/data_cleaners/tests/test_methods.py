"""Unittests for the `methods` module."""

from django.test import SimpleTestCase, TestCase
from django.contrib.contenttypes.models import ContentType
import pandas as pd
from campaigns import models as campaign_models
from search import models as search_models
from .. import methods


class TestRemoveDuplicates(SimpleTestCase):
    """Unittests for the `RemoveDuplicates` class."""

    def test_clean_invalid_model(self):
        """Test that when a module is provided for which a field map has not
        been defined, an `ImplementationError` is raised.
        """
        remove_duplicates = methods.RemoveDuplicates(
            pd.DataFrame({"a": [1, 2, 3]}), ContentType
        )
        with self.assertRaises(NotImplementedError):
            remove_duplicates.clean()

    def test_campaigns(self):
        """Test that the data for the `Campaign` model is cleaned correctly."""
        dataframe = pd.DataFrame(
            {
                "campaign_id": [1, 2, 1],
                "structure_value": ["a", "a", "a"],
                "status": ["ENABLED", "ENABLED", "DISABLED"],
            }
        )
        remove_duplicates = methods.RemoveDuplicates(
            dataframe, campaign_models.Campaign
        )
        remove_duplicates.clean()
        results = remove_duplicates.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "campaign_id": [2, 1],
                "structure_value": ["a", "a"],
                "status": ["ENABLED", "DISABLED"],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )

    def test_ad_groups(self):
        """Test that the data for the `AdGroup` model is cleaned correctly."""
        dataframe = pd.DataFrame(
            {
                "ad_group_id": [1, 2, 1],
                "campaign_id": [1, 1, 1],
                "alias": ["a", "a", "a"],
                "status": ["ENABLED", "ENABLED", "DISABLED"],
            }
        )

        remove_duplicates = methods.RemoveDuplicates(
            dataframe, campaign_models.AdGroup
        )
        remove_duplicates.clean()
        results = remove_duplicates.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "ad_group_id": [2, 1],
                "campaign_id": [1, 1],
                "alias": ["a", "a"],
                "status": ["ENABLED", "DISABLED"],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )

    def test_search_terms(self):
        """Test that the data for the `SearchTerm` model is cleaned correctly."""
        dataframe = pd.DataFrame(
            {
                "ad_group_id": [1, 2, 1],
                "campaign_id": [1, 1, 1],
                "search_term": ["a", "a", "a"],
                "cost": [1, 2, 3],
                "status": ["ENABLED", "ENABLED", "DISABLED"],
            }
        )

        remove_duplicates = methods.RemoveDuplicates(
            dataframe, search_models.SearchTerm
        )
        remove_duplicates.clean()
        results = remove_duplicates.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "ad_group_id": [2, 1],
                "campaign_id": [1, 1],
                "search_term": ["a", "a"],
                "cost": [2, 3],
                "status": ["ENABLED", "DISABLED"],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )


class TestFilterValidForeignKeys(TestCase):
    """Unittests for the `FilterValidForeignKeys` class."""

    def test_ad_group(self):
        """Test that the `clean` removes the correct data when being used for
        the `campaign_models.AdGroup` class.
        """

        # Load the Campaign model with data as the AdGroup model contains a
        # foreign key to the Campaign model.
        for i in (50, 100):
            campaign_models.Campaign.objects.create(
                id=i,
                structure_value="a",
                status="ENABLED",
            ).save()

        dataframe = pd.DataFrame(
            {
                "ad_group_id": [1, 2, 1],
                "campaign_id": [50, 100, 200],
            }
        )

        filter_valid_fks = methods.FilterValidForeignKeys(
            dataframe, campaign_models.AdGroup
        )
        filter_valid_fks.clean()
        results = filter_valid_fks.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "ad_group_id": [1, 2],
                "campaign_id": [50, 100],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )
