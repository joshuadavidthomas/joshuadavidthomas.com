from __future__ import annotations

from django.urls import path

from . import views

app_name = "dcus2024"

urlpatterns = [
    path("level1/", views.Level1FormView.as_view(), name="level-one"),
    path("date/", views.DateFormView.as_view(), name="date"),
    path(
        "password-reset/", views.PasswordResetFormView.as_view(), name="password-reset"
    ),
]
