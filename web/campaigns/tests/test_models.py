from django.test import TestCase
from .utils import get_campaign, get_ad_group


class TestCampaign(TestCase):
    """Unittests for the `Campaign` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_campaign()), str)


class TestAdGroup(TestCase):
    """Unittests for the `AdGroup` model."""

    def test__str__(self):
        """Test that the method returns a `str` instance."""
        self.assertIsInstance(str(get_ad_group()), str)
