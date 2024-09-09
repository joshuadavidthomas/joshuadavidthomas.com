from __future__ import annotations

from django import template

from talks.models import Section

register = template.Library()


@register.simple_tag(takes_context=True)
def render_section(context, section: Section):
    return template.Template(section.content).render(context)
