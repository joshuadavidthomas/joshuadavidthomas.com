from __future__ import annotations

from functools import partial

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.markdown import md
from core.models import TimeStamped

from .managers import EntryQuerySet
from .managers import PublishedEntryManager

TitleField = partial(models.CharField, max_length=255)
SlugField = partial(models.SlugField, max_length=75, blank=True, unique=True)
SummaryField = partial(models.TextField, blank=True)
ContentField = partial(models.TextField)


class Post(TimeStamped, models.Model):
    title = TitleField()
    slug = SlugField()
    tags = models.ManyToManyField("blog.Tag", blank=True)
    published_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time to publish the entry"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if self._meta.model.objects.filter(slug=self.slug).exists():  # type: ignore[attr-defined]
                self.slug += f"-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class Entry(models.Model):
    __yamdl__ = True

    title = TitleField()
    slug = SlugField()
    summary = models.TextField(blank=True)
    content = models.TextField()

    created_at = models.DateTimeField()
    published_at = models.DateTimeField(blank=True, null=True)

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.created_at.year}/{self.slug}/"

    @mark_safe
    def render_summary(self):
        return md.render(self.summary)

    @mark_safe
    def render_content(self):
        return md.render(self.content)


class PublishedEntry(Post):
    summary = SummaryField()
    content = ContentField()
    card_image = models.URLField(
        blank=True, null=True, help_text="URL to image for social media cards"
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

    objects = PublishedEntryManager()

    class Meta:
        verbose_name_plural = "published entries"

    def get_absolute_url(self):
        return f"/blog/{self.created_at.year}/{self.slug}/"

    @mark_safe
    def render_summary(self):
        return md.render(self.summary)

    @mark_safe
    def render_content(self):
        return md.render(self.content)


class Link(Post):
    url = models.URLField()
    via_title = models.CharField(max_length=255, blank=True)
    via_url = models.URLField(blank=True)
    comments = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    @mark_safe
    def render_comments(self):
        return md.render(self.comments)


class Tag(TimeStamped, models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
