from django.test import TestCase
from .utils import get_search_term


class TestSearchTerm(TestCase):
    """Unittests for the `SearchTerm` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_search_term()), str)

    def test_roas(self):
        """Test that the method calculates the RoAS for a search term
        correctly.
        """
        search_term = get_search_term(
            cost=0.5,
            conversion_value=2.0,
        )
        self.assertEqual(search_term.roas(), 4.0)

    def test_roas_0_cost(self):
        """Test that the method does not run into a ZeroDivisionError when
        the cost is 0.
        """
        search_term = get_search_term(
            cost=0.0,
            conversion_value=2.0,
        )
        self.assertEqual(search_term.roas(), 2.0)
