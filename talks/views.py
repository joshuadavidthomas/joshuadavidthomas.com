from __future__ import annotations

from django.forms.models import modelform_factory
from django.http import FileResponse
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Talk


def index(request: HttpRequest) -> HttpResponse:
    talks = Talk.objects.all()
    return render(request, "talks/index.html", {"talks": talks})


def talk(request: HttpRequest, slug: str) -> HttpResponse:
    talk = get_object_or_404(Talk, slug=slug)
    form = modelform_factory(Talk, fields=["title"])
    return render(request, "talks/talk.html", {"talk": talk, "form": form()})


def qrcode(request: HttpRequest, slug: str) -> FileResponse:
    talk = get_object_or_404(Talk, slug=slug)
    buffer = talk.make_qrcode(request)
    return FileResponse(buffer, content_type="image/svg+xml")
