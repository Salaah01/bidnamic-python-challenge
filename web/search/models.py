from django.db import models, connection
import pandas as pd
from campaigns import models as campaign_models
from data_cleaners import methods as cleaning_methods
from data_cleaners.base import clean_data


class SearchTerm(models.Model):
    date = models.DateField()
    ad_group = models.ForeignKey(
        campaign_models.AdGroup,
        on_delete=models.PROTECT,
    )
    clicks = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_value = models.DecimalField(max_digits=10, decimal_places=2)
    conversions = models.PositiveIntegerField()
    search_term = models.CharField(max_length=255)
    roas = models.FloatField(blank=True)

    class Meta:
        ordering = ("-date",)
        unique_together = ("date", "ad_group", "search_term")

    class DataCleaner:
        from campaigns.models import AdGroup

        remove_duplicates_subset_fields = [
            "date",
            "ad_group_id",
            "campaign_id",
            "search_term",
        ]
        remove_columns = ["campaign_id"]
        fk_map = {
            "ad_group_id": {
                "model": AdGroup,
                "field": "id",
            }
        }

    def __str__(self):
        return f"({self.date}) {self.ad_group}"

    def save(self, *args, **kwargs):
        """If `roas` is not set, calculate it before saving."""
        if not self.roas:
            self.roas = self.calc_roas()
        super().save(*args, **kwargs)

    @classmethod
    def load_from_dataframe(cls, dataframe: pd.DataFrame):
        """Updates or inserts records in bulk from a pandas dataframe.

        Args:
            dataframe - Pandas dataframe containing the data to be uploaded.
        """

        df = clean_data(
            dataframe,
            cls,
            [
                cleaning_methods.RemoveDuplicates,
                cleaning_methods.FilterValidForeignKeys,
                cleaning_methods.RemoveColumns,
            ],
        )
        db_table = cls._meta.db_table
        query = f"""
            INSERT INTO {db_table} (
                date,
                ad_group_id,
                clicks,
                cost,
                conversion_value,
                conversions,
                search_term,
                roas
            ) VALUES """

        params = []
        df_cols = df.columns.tolist()
        for row in df.itertuples():
            for col in df_cols:
                params.append(getattr(row, col))
            params.extend([row.conversion_value, row.cost or 1])
            query += """
                (%s, %s, %s, %s, %s, %s, %s, %s / %s),"""

        query = query.strip().rstrip(",")
        query += """
            ON CONFLICT (date, ad_group_id, search_term) DO UPDATE
            SET clicks = EXCLUDED.clicks,
                cost = EXCLUDED.cost,
                conversion_value = EXCLUDED.conversion_value,
                conversions = EXCLUDED.conversions;
            COMMIT;"""

        with connection.cursor() as cursor:
            cursor.execute(query, params)

    def calc_roas(self) -> float:
        """Calculates the Return On Ad Spend (RoAS) for the search term.
        Returns:
            float: The RoAS for the search term.
        """
        if self.cost == 0:
            return self.conversion_value
        return self.conversion_value / self.cost
