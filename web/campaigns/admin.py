from django.contrib import admin
from . import models


@admin.register(models.Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ["id", "structure_value", "status"]
    list_filter = ["status"]


@admin.register(models.AdGroup)
class AdGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "campaign", "alias", "status"]
    list_filter = ["status"]
