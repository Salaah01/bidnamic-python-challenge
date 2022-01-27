from django.test import TestCase
from .utils import get_search_term


class TestSearchTerm(TestCase):
    """Unittests for the `SearchTerm` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_search_term()), str)
