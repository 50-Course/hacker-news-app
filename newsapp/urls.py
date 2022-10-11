from __future__ import annotations

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from newsapp.views import create_jobview
from newsapp.views import create_storyview
from newsapp.views import DisplayNewsView
from newsapp.views import get_item_view

app_name = "newsapp"

urlpatterns = [
    path("home", DisplayNewsView.as_view(), name="list-news"),
    # Authentication Views
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="login"),
    # Application Urls
    path("stories/", create_storyview, name="list-items"),
    path("jobs/", create_jobview, name="list-news"),
    path("<int:id>/", get_item_view, name="get-items"),
]
