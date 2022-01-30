from datetime import date
from django.test import TransactionTestCase
import pandas as pd
from campaigns import models as campaign_models
from .. import models as search_models
from .utils import get_search_term


class TestSearchTerm(TransactionTestCase):
    """Unittests for the `SearchTerm` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_search_term()), str)

    def test_calc_roas(self):
        """Test that the method calculates the RoAS for a search term
        correctly.
        """
        search_term = get_search_term(
            cost=0.5,
            conversion_value=2.0,
        )
        self.assertEqual(search_term.calc_roas(), 4.0)

    def test_calc_roas_0_cost(self):
        """Test that the method does not run into a ZeroDivisionError when
        the cost is 0.
        """
        search_term = get_search_term(
            cost=0.0,
            conversion_value=2.0,
        )
        self.assertEqual(search_term.calc_roas(), 2.0)

    def test_load_from_dataframe(self):
        """Test that the method loads the data from a dataframe correctly."""

        # Need to firstly load other tables to ensure that the foreign keys are
        # valid.
        for i in (50, 100):
            campaign = campaign_models.Campaign.objects.create(
                id=i,
                structure_value="a",
                status="ENABLED",
            )
            campaign.save()
            campaign_models.AdGroup.objects.create(
                id=i,
                campaign=campaign,
                alias="a",
                status="ENABLED",
            ).save()

        # Prepare test data.
        today = date.today()
        dataframe = pd.DataFrame(
            {
                "date": [today, today, today, today],
                "ad_group_id": [50, 100, 50, 200],
                "campaign_id": [50, 100, 50, 200],
                "clicks": [1, 2, 3, 4],
                "cost": [0.5, 1.0, 2.0, 3.0],
                "conversion_value": [1.0, 2.0, 3.0, 4.0],
                "conversions": [1, 2, 3, 4],
                "search_term": ["a", "b", "a", "d"],
            }
        )

        # Run the method.
        search_models.SearchTerm.load_from_dataframe(dataframe)

        # Check that the data was loaded correctly.
        self.assertEqual(search_models.SearchTerm.objects.count(), 2)

        search_ad_group_50 = search_models.SearchTerm.objects.filter(
            ad_group_id=50,
        ).first()
        self.assertEqual(search_ad_group_50.clicks, 3)
        self.assertEqual(search_ad_group_50.cost, 2.0)
        self.assertEqual(search_ad_group_50.conversion_value, 3.0)
        self.assertEqual(search_ad_group_50.conversions, 3)
        self.assertEqual(search_ad_group_50.search_term, "a")

        search_ad_group_100 = search_models.SearchTerm.objects.filter(
            ad_group_id=100,
        ).first()
        self.assertEqual(search_ad_group_100.clicks, 2)
        self.assertEqual(search_ad_group_100.cost, 1.0)
        self.assertEqual(search_ad_group_100.conversion_value, 2.0)
        self.assertEqual(search_ad_group_100.conversions, 2)
        self.assertEqual(search_ad_group_100.search_term, "b")
