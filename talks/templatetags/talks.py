from __future__ import annotations

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def render_content(context, content):
    return template.Template(content).render(context)
