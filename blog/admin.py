from __future__ import annotations

from django.contrib import admin
from django.contrib import messages
from django.db import models

from core.admin.widgets import EasyMDEWidget

from .models import Link
from .models import PublishedEntry
from .models import Tag


@admin.register(PublishedEntry)
class PublishedEntryAdmin(admin.ModelAdmin):
    actions = ["duplicate_entry"]
    fields = [
        "title",
        "slug",
        "summary",
        "body",
        "tags",
        "card_image",
        "created_at",
        "updated_at",
        "published_at",
    ]
    formfield_overrides = {
        models.TextField: {"widget": EasyMDEWidget(width="100%", height="500px")}
    }
    list_display = ["title", "created_at", "updated_at", "published_at"]
    readonly_fields = ["slug", "created_at", "updated_at"]

    @admin.action(description="Duplicate entry")
    def duplicate_entry(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "%d entries selected, only one entry can be duplicated at a time."
                % queryset.count(),
                messages.ERROR,
            )
            return
        entry = queryset.first()
        PublishedEntry.objects.create_duplicate(entry)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "slug",
        "url",
        "via_title",
        "via_url",
        "comments",
        "tags",
        "created_at",
        "updated_at",
        "published_at",
    ]
    list_display = ["title", "created_at", "updated_at", "published_at"]
    readonly_fields = ["slug", "created_at", "updated_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
