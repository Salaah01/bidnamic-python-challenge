"""Bidnamic URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        'raw-schema',
        get_schema_view(
            title="Bidnamic API",
            description="API for Bidnamic.",
            version="1.0.0"
        ),
        name='openapi-schema'
    ),
    path(
        '',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'
    ),
    path("search/", include("search.urls")),
]
