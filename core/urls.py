"""core URL Configuration

Maintainer:  Eri Adeodu (@50-Course)
"""
from __future__ import annotations

from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Documentation Endpoint
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/api-docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema",
    ),
    # API Urls
    path("api/v1/", include("api.urls")),
    # Frontend Urls
    path("", include("newsapp.urls")),
]
