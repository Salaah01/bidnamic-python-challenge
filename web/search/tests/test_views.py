"""Unittest for the views module."""

import typing as _t
from django.urls import reverse
from django.db.models import QuerySet
from rest_framework.test import (
    APIRequestFactory,
    APITestCase,
    RequestsClient,
    APILiveServerTestCase,
)
from api import exceptions as api_exceptions
from .. import views, models as search_models
from .utils import get_search_term


def load_test_data() -> QuerySet[search_models.SearchTerm]:
    for i in range(1, 21):
        get_search_term(search_term=str(i))
    return search_models.SearchTerm.objects.all()


class BaseLiveTestCase(APILiveServerTestCase):
    """Base class for live tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_test_data()

    def get_request(
        self,
        url: str,
        json_payload: _t.Optional[dict] = None,
    ) -> RequestsClient.get:
        """Creates a request object with the given query params and json
        payload.

        Args:
            url - The url to send the request to.
            json_payload - The json payload to use.
        Returns:
            The request object.
        """
        request = RequestsClient().get(
            self.live_server_url + url, json=json_payload or {}
        )
        return request


class TestApplyLimit(APITestCase):
    """Unittests for the `apply_limit` function."""

    @classmethod
    def setUpTestData(cls):
        """Loads testdata"""
        cls.queryset = load_test_data()

    @staticmethod
    def get_request(
        query_params: _t.Optional[dict] = None,
        json_payload: _t.Optional[dict] = None,
    ) -> APIRequestFactory.get:
        """Creates a request object with the given query params and json
        payload.

        Args:
            query_params - The query paramaters to use.
            json_payload - The json payload to use.
        Returns:
            The request object.
        """

        request = APIRequestFactory().get("/", query_params or {})
        request.data = json_payload or {}
        return request

    def test_applies_default_limit(self):
        """Test that the `apply_limit` function applies a default limit if none
        is provided.
        """

        # Test using a normal get request.
        self.assertEqual(
            views.apply_limit(self.get_request(), self.queryset).count(), 10
        )

    def test_accepts_all_as_limit(self):
        """Test that the `apply_limit` function accepts the `all` query
        parameter.
        """

        # Test using a normal get request.
        self.assertEqual(
            views.apply_limit(
                self.get_request(query_params={"limit": "all"}), self.queryset
            ).count(),
            self.queryset.count(),
        )

        # Test a JSON get request.
        self.assertEqual(
            views.apply_limit(
                self.get_request(json_payload={"limit": "all"}), self.queryset
            ).count(),
            self.queryset.count(),
        )

    def test_applies_limit_from_query_param(self):
        """Test that the `apply_limit` function applies a limit from a query
        parameter.
        """

        # Test using a normal get request.
        self.assertEqual(
            views.apply_limit(
                self.get_request(query_params={"limit": "5"}), self.queryset
            ).count(),
            5,
        )

        # Test a JSON get request.
        self.assertEqual(
            views.apply_limit(
                self.get_request(json_payload={"limit": "5"}), self.queryset
            ).count(),
            5,
        )

    def test_invalid_param(self):
        """Test that the `apply_limit` function raises an error if an invalid
        query parameter is provided.
        """

        # Test using a normal get request.
        with self.assertRaises(api_exceptions.ValidationError):
            views.apply_limit(
                self.get_request(query_params={"limit": "invalid"}),
                self.queryset,
            )

        # Test a JSON get request.
        with self.assertRaises(api_exceptions.ValidationError):
            views.apply_limit(
                self.get_request(json_payload={"limit": "invalid"}),
                self.queryset,
            )


class TestRoasByStructuredValue(BaseLiveTestCase):
    """Unittests for the `roas_by_structured_value` view."""

    def get_request(
        self, structured_value: _t.Optional[str] = None, is_json: bool = False
    ) -> APIRequestFactory.get:
        """Overrides the `get_request` method by setting the `url` argument
        to the `roas_by_structured_value` view as well as simplifying the
        args making it specific to this test.

        Args:
            structured_value - The structured value to use.
            is_json - Whether the request should be a JSON request.

        Returns:
            The request object.
        """

        if structured_value is None:
            url = reverse("roas-by-structured-value")
            json_data = {}
        elif is_json:
            url = reverse("roas-by-structured-value")
            json_data = {"structured_value": structured_value}
        else:
            url = reverse("roas-by-structured-value", args=[structured_value])
            json_data = {}

        return super().get_request(url, json_payload=json_data)

    def test_no_structured_value(self):
        """Test that a 400 response is returned if no `structured_value` is
        provided.
        """
        self.assertEqual(self.get_request().status_code, 400)

    def test_with_structured_data_arg(self):
        """Test that a 200 response is returned if a `structured_value` is
        provided as part of the url (as an argument).
        """
        self.assertEqual(self.get_request("structured_value").status_code, 200)

    def test_with_json_structured_data(self):
        """Test that a 200 response is returned if a `structured_value` is
        provided as part of the JSON payload.
        """
        self.assertEqual(
            self.get_request("structured_value", is_json=True).status_code, 200
        )
