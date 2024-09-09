from __future__ import annotations

from django.urls import path

from . import views

app_name = "talks"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.talk, name="talk"),
    path("<slug:slug>/qrcode.svg", views.qrcode, name="qrcode"),
]
