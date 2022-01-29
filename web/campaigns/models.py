from django.db import models, connection
import pandas as pd
from data_cleaners import methods as cleaning_methods
from data_cleaners.base import clean_data


class Campaign(models.Model):
    """Represents a campaign."""

    structure_value = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}: {self.status}"

    class DataCleaner:
        remove_duplicates_subset_fields = ["campaign_id"]
        rename_headers_header_map = {
            "campaign_id": "id",
        }

    @classmethod
    def load_from_dataset(cls, dataframe: pd.DataFrame):
        """Updates or inserts records in bulk from a pandas dataframe.

        Args:
            dataframe - Pandas dataframe containing thedata to be uploaded.
        """

        df = clean_data(
            dataframe,
            cls,
            [
                cleaning_methods.RemoveDuplicates,
                cleaning_methods.RenameHeaders,
            ],
        )
        db_table = cls._meta.db_table

        # Build a multi insert query where if the primary key already exists
        # update the record, otherwise insert a new record.
        params = []
        query = f"""BEGIN;
                    INSERT INTO {db_table} (id, structure_value, status) VALUES 
                    """

        insert_query = """(%s, %s, %s),"""

        for row in df.itertuples():
            params.append(row.id)
            params.append(row.structure_value)
            params.append(row.status)
            query += insert_query

        query = query.strip().rstrip(",")
        query += """ON CONFLICT (id) DO UPDATE
                    SET structure_value = EXCLUDED.structure_value,
                        status = EXCLUDED.status;
                    COMMIT;"""

        with connection.cursor() as cursor:
            cursor.execute(query, params)


class AdGroup(models.Model):
    """Represents an ad group."""

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    class DataCleaner:
        remove_duplicates_subset_fields = ["ad_group_id", "campaign_id"]
        rename_headers_header_map = {
            "ad_group_id": "id",
        }

    def __str__(self):
        return f"{self.id}-{self.campaign.id}: {self.status}"
