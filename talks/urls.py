from __future__ import annotations

from django.urls import include
from django.urls import path

from . import views

app_name = "talks"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.talk, name="talk"),
    path("<slug:slug>/form/", views.talk_form, name="talk-form"),
    path("<slug:slug>/qrcode.svg", views.qrcode, name="qrcode"),
    path("dcus2024/", include("talks.dcus2024.urls")),
]
