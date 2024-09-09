from __future__ import annotations

from django.contrib import admin

from .models import Section
from .models import Talk


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "colors"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["talk", "title", "order"]
    ordering = ["-order"]
