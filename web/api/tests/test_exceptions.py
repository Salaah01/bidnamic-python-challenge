"""Unittests for the `exceptions` module."""

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from .. import exceptions


class TestBaseException(SimpleTestCase):
    """Unittests for the `base_exception` function."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_base_exception_no_args(self):
        """Test that the function is able to handle calls without any optional
        arguments.
        """
        req = self.factory.get("/", {"foo": "bar"})
        res = exceptions.base_exception(req)

        self.assertEqual(
            res,
            {"metadata": {"query_params": {"foo": "bar"}}, "data": {}, "error": None},
        )

    def test_base_exception_with_args(self):
        """Test that the function returns the correct value when provided
        arguments.
        """
        req = self.factory.get("/", {"foo": "bar"})
        res = exceptions.base_exception(
            req, metadata={"baz": "qux"}, data={"foo": "bar"}, error="error"
        )

        self.assertEqual(
            res,
            {
                "metadata": {"query_params": {"foo": "bar"}, "baz": "qux"},
                "data": {"foo": "bar"},
                "error": "error",
            },
        )


class TestExceptions(SimpleTestCase):
    """Test the exception classes. All of these classes should behave in a
    very similar way, so are all grouped within this test class.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_validation_error(self):
        """Test that when a `ValidationError` is raised, the correct response
        is returned.
        """

        exception_args = {
            "request": Request(self.factory.get("/"), {"foo": "bar"}),
            "metadata": {"results": 2},
            "data": {"a": 1, "b": 2},
            "error": "error",
        }

        with self.assertRaises(exceptions.ValidationError) as err:
            raise exceptions.ValidationError(**exception_args)

            self.assertEqual(err.exception.status_code, 400)
            self.assertEqual(
                err.exception.response,
                {
                    "metadata": {"query_params": {"foo": "bar"}, "results": 2},
                    "data": {"a": 1, "b": 2},
                    "error": "error",
                },
            )

    def test_not_found_error(self):
        """Test that when a `NotFoundError` is raised, the correct response
        is returned.
        """

        exception_args = {
            "request": Request(self.factory.get("/"), {"foo": "bar"}),
            "metadata": {"results": 2},
            "data": {"a": 1, "b": 2},
            "error": "error",
        }

        with self.assertRaises(exceptions.NotFoundError) as err:
            raise exceptions.NotFoundError(**exception_args)

            self.assertEqual(err.exception.status_code, 404)
            self.assertEqual(
                err.exception.response,
                {
                    "metadata": {"query_params": {"foo": "bar"}, "results": 2},
                    "data": {"a": 1, "b": 2},
                    "error": "error",
                },
            )
