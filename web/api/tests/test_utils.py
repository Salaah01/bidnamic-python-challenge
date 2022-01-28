"""Unittests for the `utils` module."""

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from .. import utils


class TestBuildMetadata(SimpleTestCase):
    """Unittests for the `build_metadata` function."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_build_metadata_no_params(self):
        """Test that the function support a simple get request without any
        query parameters.
        """
        self.assertEqual(
            utils.build_metadata(self.factory.get("/")), {"query_params": {}}
        )

    def test_build_metadata_with_params(self):
        """Test that the function support a simple get request with query
        parameters.
        """
        self.assertEqual(
            utils.build_metadata(self.factory.get("/", {"foo": "bar"})),
            {"query_params": {"foo": "bar"}},
        )
