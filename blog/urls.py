from __future__ import annotations

from django.urls import path

from . import views
from . import feeds

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<slug:slug>/", views.entry, name="entry"),
    path("tag/<slug:slug>/", views.tag),
    path("feed/", feeds.EntriesFeed(), name="feed"),
]
