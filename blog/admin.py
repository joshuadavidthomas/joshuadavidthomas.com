from __future__ import annotations

from django.contrib import admin
from django.contrib import messages
from django.db import models

from core.admin.widgets import EasyMDEWidget

from .models import Entry
from .models import Tag


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    actions = ["duplicate_entry"]
    formfield_overrides = {
        models.TextField: {"widget": EasyMDEWidget(width="100%", height="500px")}
    }
    list_display = ["title", "created_at", "updated_at", "published_at"]
    readonly_fields = ["slug", "created_at", "updated_at"]

    @admin.display(description="Duplicate entry")
    def duplicate_entry(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                f"{queryset.count()} entries selected, only one entry can be duplicated at a time.",
                messages.ERROR,
            )
            return
        entry = queryset.first()
        Entry.objects.create_duplicate(entry)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    readonly_fields = ["slug", "created_at", "updated_at"]
