"""Unitests for the `base` module."""

from types import SimpleNamespace
import pandas as pd
from django.test import SimpleTestCase
from .. import base


# Test Strategies.
# They don't necessarily clean, but they do manipulate the dataframe in some
# way.
class ReverseStrategy(base.CleaningStrategy):
    """A strategy that reverses the dataframe."""

    def clean(self) -> pd.DataFrame:
        """Reverses the dataframe in place."""
        self.dataframe = self.dataframe.iloc[::-1]


class FirstTwoRowsStrategy(base.CleaningStrategy):
    """A strategy that shrinks the dataframe to only the first two rows."""

    def clean(self) -> pd.DataFrame:
        """Shrinks the dataframe to only the first two rows."""
        self.dataframe = self.dataframe.iloc[:2]


# Unittests


class TestCleaningStrategy(SimpleTestCase):
    """Unittests for the `CleaningStrategy` class."""

    def test_can_use_cleaner_pass(self):
        """Test that the `can_use_cleaner` method indicates `True` when a
        model has the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None, model=SimpleNamespace(DataCleaner=1)
        )
        self.assertEqual(
            base.CleaningStrategy.can_use_cleaner(instance), (True, None)
        )

    def test_can_use_cleaner_fail(self):
        """Test that the `can_use_cleaner` method indicates `False` when a
        model does not have the attributes the method expects.
        """

        instance = SimpleNamespace(dataframe=None, model=SimpleNamespace())
        self.assertEqual(
            base.CleaningStrategy.can_use_cleaner(instance),
            (False, "The model does not have a DataCleaner class."),
        )

    def test_validate_model_pass(self):
        """Test that the `validate_model` method does not raise an error when
        the model has the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None,
            model=SimpleNamespace(DataCleaner=1),
            can_use_cleaner=lambda: (True, None),
        )
        base.CleaningStrategy.validate_model(instance)

    def test_validate_model_fail(self):
        """Test that the `validate_model` method raises an error when the
        model does not have the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None,
            model=SimpleNamespace(),
            can_use_cleaner=lambda: (False, "Failed"),
        )
        with self.assertRaises(NotImplementedError):
            base.CleaningStrategy.validate_model(instance)


class TestCleanData(SimpleTestCase):
    """Unittests for the `clean_data` function."""

    def test_can_apply_strategies(self):
        """Test that the method is able to apply various cleaning strategies on
        a dataframe.
        """

        # Create a test dataframe.
        dataframe = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
                "col3": [7, 8, 9],
            }
        )

        # make a copy of the dataframe to test that the strategies are applied
        # in the correct order.
        results = base.clean_data(
            dataframe, None, [ReverseStrategy, FirstTwoRowsStrategy]
        ).reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "col1": [3, 2],
                "col2": [6, 5],
                "col3": [9, 8],
            }
        )
        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )

    def test_no_mutations(self):
        """Test that the original dataframe is not mutated."""
        dataframe = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
                "col3": [7, 8, 9],
            }
        )

        dataframe_copy = dataframe.copy()
        base.clean_data(dataframe, None, [ReverseStrategy])
        self.assertTrue(dataframe.equals(dataframe_copy))
