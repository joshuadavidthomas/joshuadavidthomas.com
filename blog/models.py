from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.markdown import md
from core.models import TimeStamped

from .managers import EntryManager


class Entry(TimeStamped, models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75, blank=True)
    summary = models.TextField()
    body = models.TextField()
    card_image = models.URLField(
        blank=True, null=True, help_text="URL to image for social media cards"
    )
    tags = models.ManyToManyField("blog.Tag", blank=True)
    published_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time to publish the entry"
    )
    is_draft = models.GeneratedField(
        expression=models.Case(
            models.When(
                published_at__isnull=False,
                then=False,
            ),
            default=True,
        ),
        output_field=models.BooleanField(),
        db_persist=False,
        help_text="Draft entries do not show in index pages but can be visited directly if you know the URL",
    )

    objects = EntryManager()

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

    @mark_safe
    def render_summary(self):
        return md.render(self.summary)

    @mark_safe
    def render_body(self):
        return md.render(self.body)


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
