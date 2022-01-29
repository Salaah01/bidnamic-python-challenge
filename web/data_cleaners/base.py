"""This module constains an abstract base class for data cleaning strategies
that is used to define new cleaning strategies. It also contains the main
function that is used to run the cleaning strategy.
"""

import typing as _t
import pandas as pd
from django.db.models import Model
from abc import ABC, abstractmethod


class CleaningStrategy(ABC):
    """This class defines the strategy for cleaning data."""

    def __init__(self, dataframe: pd.DataFrame, model: Model):
        """Initialize the cleaning strategy.

        Args:
            dataframe: A pandas dataframe.
            model: A django model.
        """
        self.dataframe = dataframe
        self.model = model
        self.dataset_has_been_reversed = False

    @abstractmethod
    def clean(self) -> pd.DataFrame:
        """This method cleans the data and returns a cleaned dataframe

        Args:
            dataframe - The dataframe to be cleaned.
            model - The model which the data is being cleaned for.

        Returns:
            The cleaned dataframe.
        """
        pass


def clean_data(
    dataframe: pd.DataFrame, model: Model, strategies: _t.List[CleaningStrategy]
) -> pd.DataFrame:
    """This function cleans the data using the given strategies.

    Args:
        dataframe: A pandas dataframe.
        model: A django model.
        strategies: A list of cleaning strategies.

    Returns:
        The cleaned dataframe.
    """

    df = dataframe.copy()
    for strategy in strategies:
        strat = strategy(df, model)
        strat.clean()
        df = strat.dataframe
    return df
