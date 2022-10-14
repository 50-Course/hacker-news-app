from __future__ import annotations

from django.urls import path

from .routers import router
from api.views import GetLatestNewsAPIView
from api.views import UpdateorDeleteNewsAPIView

urlpatterns = [
    path("news/", GetLatestNewsAPIView.as_view(), name="get_news"),
    path(
        "news/<int:id>",
        UpdateorDeleteNewsAPIView.as_view(),
        name="news-detail",
    ),
]

urlpatterns += router.urls
