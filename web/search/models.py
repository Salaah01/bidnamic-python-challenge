from django.db import models
from campaigns import models as campaign_models


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

    class Meta:
        ordering = ("-date",)

    class DataCleaner:
        remove_duplicates_subset_fields = [
            "ad_group_id",
            "campaign_id",
            "search_term",
        ]
        remove_columns = ["campaign_id"]

    def __str__(self):
        return f"({self.date}) {self.ad_group}"

    def roas(self) -> float:
        """Calculates the Return On Ad Spend (RoAS) for the search term.
        Returns:
            float: The RoAS for the search term.
        """
        if self.cost == 0:
            return self.conversion_value
        return self.conversion_value / self.cost
