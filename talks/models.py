from __future__ import annotations

from io import BytesIO
from pathlib import Path

import qrcode
from django.contrib.sites.models import Site
from django.db import models
from django.http import HttpRequest
from django_twc_toolbox.urls import reverse
from qrcode.image.svg import SvgPathImage

from core.yamdl.loader import ModelLoader


class Talk(models.Model):
    __yamdl__ = True

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75, blank=True, unique=True)
    colors = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("talks:talk", kwargs={"slug": self.slug})

    def make_qrcode(self, request: HttpRequest | None = None):
        if request:
            absolute_url = request.build_absolute_uri(self.get_absolute_url())
        else:
            current_site = Site.objects.get_current()
            absolute_url = f"https://{current_site.domain}{self.get_absolute_url()}"

        img = qrcode.make(absolute_url, image_factory=SvgPathImage)
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return buffer

    @classmethod
    def from_yaml(cls, file_path: Path, **data: object):
        talk, _ = cls.objects.get_or_create(
            slug=file_path.parent.stem,
            defaults={"title": data.get("talk_title"), "colors": data.get("class")},
        )

        if file_path.suffix in ModelLoader.EXT_MARKDOWN and file_path.is_file():
            Section.objects.create(
                talk=talk,
                title=data.get("section_title"),
                order=file_path.stem,
                colors=data.get("class", "bg-white text-gray-900"),
                content=data.get("content"),
            )

        return talk


class Section(models.Model):
    __yamdl__ = True

    talk = models.ForeignKey(
        "talks.Talk", on_delete=models.DO_NOTHING, related_name="sections"
    )
    title = models.CharField(max_length=255, null=True)
    order = models.PositiveSmallIntegerField()
    colors = models.CharField(max_length=255)
    content = models.TextField()
