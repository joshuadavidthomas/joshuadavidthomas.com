from __future__ import annotations

from attrs import define


@define
class SocialItem:
    title: str
    url: str
    icon: str = "exclamation-triangle"
    icon_template: str = ""
