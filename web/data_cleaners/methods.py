"""This module contains shared methods for cleaning data."""

import typing as _t
import pandas as pd
from .base import CleaningStrategy


class RemoveDuplicates(CleaningStrategy):
    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(
            self.model.DataCleaner, "remove_duplicates_subset_fields"
        )
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.remove_duplicates_subset_fields`  "
                "                   attribute.",
            )
        return True, None

    def clean(self) -> pd.DataFrame:
        """Deletes duplicate data from the dataframe keeping on the last row."""
        self.validate_model()
        self.dataframe.drop_duplicates(
            subset=self.model.DataCleaner.remove_duplicates_subset_fields,
            keep="last",
            inplace=True,
        )


class RenameHeaders(CleaningStrategy):
    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(self.model.DataCleaner, "rename_headers_header_map")
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.rename_headers_header_map`        "
                "             attribute.",
            )
        return True, None

    def clean(self) -> pd.DataFrame:
        """Renames the headers of the dataframe."""
        self.validate_model()
        self.dataframe.rename(
            columns=self.model.DataCleaner.rename_headers_header_map,
            inplace=True,
        )
