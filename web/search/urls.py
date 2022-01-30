"""Search URL Configuration."""

from django.urls import path
from . import views

urlpatterns = [
    path(
        "roas/by-structured-value/",
        views.roas_by_structured_value,
        name="roas-by-structured-value",
    ),
    path(
        "roas/by-structured-value/<str:structured_value>/",
        views.roas_by_structured_value,
        name="roas-by-structured-value",
    ),
    path("roas/by-alias/", views.roas_by_alias, name="roas-by-alias"),
    path(
        "roas/by-alias/<str:alias>/", views.roas_by_alias, name="roas-by-alias"
    ),
]
