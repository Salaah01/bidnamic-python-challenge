from django.db import models


class Campaign(models.Model):
    """Represents a campaign."""

    structure_value = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}: {self.status}"


class AdGroup(models.Model):
    """Represents an ad group."""

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}-{self.campaign.id}: {self.status}"
