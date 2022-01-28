"""Unittests for the `response` module."""

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from .. import response


class TestBaseResponse(SimpleTestCase):
    """Unittests for the `base_response` function."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_base_response_no_args(self):
        """Test that the `base_response` function is able to create a simple
        response without any arguments.
        """
        self.assertEqual(
            response.base_response(self.factory.get("/")),
            {"metadata": {"query_params": {}}, "data": {}},
        )

    def test_base_response_with_args(self):
        """Test that the `base_response` function is able to create a simple
        response with arguments.
        """
        res = response.base_response(
            self.factory.get("/", {"foo": "bar"}), metadata={"baz": "qux"}
        )
        self.assertEqual(
            res,
            {"metadata": {"query_params": {"foo": "bar"}, "baz": "qux"}, "data": {}},
        )


class TestSuccessResponse(SimpleTestCase):
    """Unittests for the `success` function."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_success_response_no_args(self):
        """Test that the function is able to create a response object when the
        function is not provided any optional arguments.
        """
        req = self.factory.get("/", {"foo": "bar"})
        res = response.success(req)

        # Despite not having any args, the function should still able to
        # maintain the API response format.
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data, {"metadata": {"query_params": {"foo": "bar"}}, "data": {}}
        )

    def test_success_response_with_args(self):
        """Test that the function is able to create a response object when the
        function is provided additional arguments.
        """
        req = self.factory.get("/", {"foo": "bar"})
        res = response.success(
            request=req, metadata={"results_count": 2}, data={"a": 1, "b": 2}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data,
            {
                "metadata": {"query_params": {"foo": "bar"}, "results_count": 2},
                "data": {"a": 1, "b": 2},
            },
        )

    def test_support_multiple_data_types(self):
        """Test that the function is able to create a response object when the
        function is provided multiple data types.
        """
        req = self.factory.get("/", {"foo": "bar"})
        expected_metadata = {"query_params": {"foo": "bar"}}

        # Test with integer
        res = response.success(request=req, status=200, data=1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {"metadata": expected_metadata, "data": 1})

        # Test with string
        res = response.success(request=req, status=200, data="foo")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {"metadata": expected_metadata, "data": "foo"})

        # Test with list
        res = response.success(request=req, status=200, data=[1, 2, 3])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {"metadata": expected_metadata, "data": [1, 2, 3]})
