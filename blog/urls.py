from __future__ import annotations

from django.urls import path

from . import feeds
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<slug:slug>/", views.entry, name="entry"),
    path("tag/<slug:slug>/", views.tag),
    path("feed/", feeds.EntriesFeed(), name="feed"),
]
