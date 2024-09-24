from __future__ import annotations

from django.urls import path

from . import views

app_name = "dcus2024"

urlpatterns = [
    path("level1/", views.Level1FormView.as_view(), name="level-one"),
    path("django52/", views.ComingInDjango52FormView.as_view(), name="django52"),
    path("date/", views.DateFormView.as_view(), name="date"),
    path(
        "password-reset/1/",
        views.PasswordResetFormView1.as_view(),
        name="password-reset-1",
    ),
    path(
        "password-reset/2/",
        views.PasswordResetFormView2.as_view(),
        name="password-reset-2",
    ),
    path(
        "password-reset/3/",
        views.PasswordResetFormView3.as_view(),
        name="password-reset-3",
    ),
    path(
        "password-reset/4/",
        views.PasswordResetFormView4.as_view(),
        name="password-reset-4",
    ),
    path(
        "password-reset/5/",
        views.PasswordResetFormView5.as_view(),
        name="password-reset-5",
    ),
    path(
        "password-reset/6/",
        views.PasswordResetFormView6.as_view(),
        name="password-reset-6",
    ),
    path(
        "password-reset/7/",
        views.PasswordResetFormView7.as_view(),
        name="password-reset-7",
    ),
    path(
        "password-reset/8/",
        views.PasswordResetFormView8.as_view(),
        name="password-reset-8",
    ),
]
