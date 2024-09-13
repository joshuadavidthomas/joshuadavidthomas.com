from __future__ import annotations

from django.contrib import admin

from .models import Talk


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
