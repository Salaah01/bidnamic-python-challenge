"""This module contains shared methods for cleaning data."""

import pandas as pd
from .base import CleaningStrategy
from campaigns import models as campaign_models
from search import models as search_models


class RemoveDuplicates(CleaningStrategy):
    subset_model_fields_map = {
        campaign_models.Campaign: ["campaign_id"],
        campaign_models.AdGroup: ["ad_group_id", "campaign_id", "alias"],
        search_models.SearchTerm: [
            "ad_group_id",
            "campaign_id",
            "search_term",
        ],
    }

    def clean(self) -> pd.DataFrame:
        """Deletes duplicate data from the dataframe keeping on the last row.
        """

        if self.model not in self.subset_model_fields_map:
            raise NotImplementedError(
                f"{self.model} is not supported by RemoveDuplicates"
            )

        self.dataframe.drop_duplicates(
            subset=self.subset_model_fields_map[self.model],
            keep="last",
            inplace=True,
        )
