from __future__ import annotations

from io import BytesIO
from pathlib import Path

import qrcode
from django.contrib.sites.models import Site
from django.db import models
from django.http import HttpRequest
from django_twc_toolbox.urls import reverse
from qrcode.image.svg import SvgPathImage


class Talk(models.Model):
    __yamdl__ = True

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75, blank=True, unique=True)
    description = models.TextField()
    stinger = models.TextField(default="Thanks!")
    content = models.TextField()
    slides_url = models.URLField(blank=True, default="")
    video_url = models.URLField(blank=True, default="")

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
        return cls.objects.create(slug=file_path.stem, **data)
