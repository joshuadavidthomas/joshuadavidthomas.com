from __future__ import annotations

from django.contrib import admin

from .models import Entry
from .models import Tag


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "updated_at", "is_draft"]
    readonly_fields = ["slug", "created_at", "updated_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    readonly_fields = ["slug", "created_at", "updated_at"]
