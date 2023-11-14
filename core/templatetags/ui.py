from __future__ import annotations

from django import template
from django.conf import settings

from core.navigation import Navigation

register = template.Library()


@register.inclusion_tag("partials/navigation.html", takes_context=True)
def navigation(context):
    navigation = Navigation(
        items=settings.NAVIGATION,
        request=context["request"],
    )
    return {"items": navigation.items}


@register.inclusion_tag("partials/social.html")
def social():
    return {"items": settings.SOCIALS}
