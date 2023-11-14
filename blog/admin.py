from __future__ import annotations

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Entry
from .models import Tag


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    actions = ["duplicate_entry"]
    list_display = ["title", "created_at", "updated_at", "is_draft"]
    readonly_fields = ["slug", "created_at", "updated_at"]

    @admin.display(description="Duplicate entry")
    def duplicate_entry(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                ngettext(
                    "%d entries selected, only one entry can be duplicated at a time.",
                    queryset.count(),
                ),
                messages.ERROR,
            )
            return
        entry = queryset.first()
        Entry.objects.create_duplicate(entry)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    readonly_fields = ["slug", "created_at", "updated_at"]
