from __future__ import annotations

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavItem


class MainNav(Nav):
    template_name = "partials/navigation.html"
    items = [
        NavItem(title="Home", url="index"),
        NavItem(title="Blog", url="blog:index"),
        NavItem(title="Talks", url="talks:index"),
        NavItem(
            title="Admin",
            url="admin:index",
            permissions=["is_staff"],
            extra_context={"boost": False},
        ),
    ]


class SocialNav(Nav):
    template_name = "partials/social.html"
    items = [
        NavItem(
            title="Email",
            url="mailto:hello@joshthomas.dev",
            extra_context={"icon": "envelope"},
        ),
        NavItem(
            title="Mastodon",
            url="https://joshthomas.dev/@josh",
            extra_context={"icon_template": "partials/mastodon.svg"},
        ),
        NavItem(
            title="GitHub",
            url="https://github.com/joshuadavidthomas",
            extra_context={"icon_template": "partials/github.svg"},
        ),
        NavItem(
            title="LinkedIn",
            url="https://www.linkedin.com/in/joshua-thomas-b1745a16/",
            extra_context={"icon_template": "partials/linkedin.svg"},
        ),
        NavItem(
            title="RSS",
            url="blog:feed",
            extra_context={"icon_template": "partials/rss.svg"},
        ),
    ]
