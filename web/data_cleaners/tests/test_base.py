"""Unitests for the `base` module."""

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
