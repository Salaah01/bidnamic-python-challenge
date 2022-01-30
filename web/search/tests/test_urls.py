"""Unittest for the url module."""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class TestUrls(SimpleTestCase):
    """Unittests to check that the urls resolve the correct views."""

    def test_roas_by_structured_value(self):
        """Test that the `roas_by_structured_value` url resolves to the correct
        view.
        """
        self.assertEqual(
            resolve(reverse("roas-by-structured-value")).func,
            views.roas_by_structured_value,
        )

    def test_roas_by_structured_value_with_arg(self):
        """Test that the `roas_by_structured_value` url resolves to the correct
        view where the url contains an argument.
        """
        self.assertEqual(
            resolve(reverse("roas-by-structured-value", args=["a"])).func,
            views.roas_by_structured_value,
        )

    def test_roas_by_alias(self):
        """Test that the `roas_by_alias` url resolves to the correct view."""
        self.assertEqual(
            resolve(reverse("roas-by-alias")).func, views.roas_by_alias
        )

    def test_roas_by_alias_with_arg(self):
        """Test that the `roas_by_alias` url resolves to the correct view where
        the url contains an argument.
        """
        self.assertEqual(
            resolve(reverse("roas-by-alias", args=["a"])).func,
            views.roas_by_alias,
        )
