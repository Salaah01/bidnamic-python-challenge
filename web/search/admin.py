from django.contrib import admin
from . import models


@admin.register(models.SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "ad_group",
        "clicks",
        "cost",
        "conversion_value",
        "conversions",
        "search_term",
        "roas",
    ]
    list_filter = ["date"]
    ordering = ["-date"]
    search_fields = ["search_term"]
    date_hierarchy = "date"
    raw_id_fields = ["ad_group"]
