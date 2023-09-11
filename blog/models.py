from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.markdown import md
from core.models import TimeStamped

from .managers import EntryQuerySet


class Entry(TimeStamped, models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75, blank=True)
    summary = models.TextField()
    body = models.TextField()
    card_image = models.URLField(
        blank=True, null=True, help_text="URL to image for social media cards"
    )
    tags = models.ManyToManyField("blog.Tag", blank=True)
    is_draft = models.BooleanField(
        default=False,
        help_text="Draft entries do not show in index pages but can be visited directly if you know the URL",
    )

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self._set_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.created_at.year}/{self.slug}/"

    def _set_slug(self) -> None:
        self.slug = slugify(self.title)
        if Entry.objects.filter(slug=self.slug).exists():
            self.slug += f"-{timezone.now().strftime('%Y%m%d%H%M%S')}"

    @property
    def summary_rendered(self):
        return mark_safe(md.render(self.summary))

    @property
    def summary_text(self):
        return strip_tags(md.render(self.summary))

    @property
    def body_rendered(self):
        return mark_safe(md.render(self.body))


class Tag(TimeStamped, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}/"
