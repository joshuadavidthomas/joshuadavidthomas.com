from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from health_check.views import MainView

from core import views as core_views

urlpatterns = [
    path(".well-known/security.txt", core_views.security_txt),
    path("robots.txt", core_views.robots_txt),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("health/", MainView.as_view()),
    path("talks/", include("talks.urls")),
    path("404/", core_views.custom_error_404, name="404"),
    path("500/", core_views.custom_error_500, name="500"),
    re_path(r"^(?P<path>.*)$", core_views.content),
    path("", core_views.index, name="index"),
]

handler404 = "core.views.custom_error_404"  # noqa: F811
handler500 = "core.views.custom_error_500"  # noqa: F811


if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ] + urlpatterns
