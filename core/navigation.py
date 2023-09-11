from __future__ import annotations

from attrs import define
from django.http import HttpRequest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


@define
class Navigation:
    items: list[NavGroup | NavItem]
    request: HttpRequest

    def __attrs_post_init__(self) -> None:
        self.items = [item for item in self.items if self._check_item_visibility(item)]

        for item in self.flat_items:
            url = item.get_url()
            if self._check_item_active(url):
                item.active = True

    def _check_item_visibility(self, item) -> bool:
        user_is_authenticated = getattr(self.request.user, "is_authenticated", False)
        user_is_staff = getattr(self.request.user, "is_staff", False)
        user_is_superuser = getattr(self.request.user, "is_superuser", False)

        if isinstance(item, NavItem):
            if (
                (item.is_authenticated and not user_is_authenticated)
                or (item.is_staff and not user_is_staff)
                or (item.is_superuser and not user_is_superuser)
            ):
                return False
        elif isinstance(item, NavGroup):
            item.items = [
                sub_item
                for sub_item in item.items
                if self._check_item_visibility(sub_item)
            ]
            if not item.items:
                return False
        return True

    def _check_item_active(self, url) -> bool:
        if self.request.path == url:
            return True
        return False

    @property
    def flat_items(self) -> list[NavItem]:
        ret = []
        for item in self.items:
            if isinstance(item, NavGroup):
                ret.extend(item.items)
            else:
                ret.append(item)
        return ret


@define
class NavGroup:
    title: str
    items: list[NavItem]


@define
class NavItem:
    title: str
    url: str = "#"
    active: bool = False
    is_authenticated: bool = False
    is_staff: bool = False
    is_superuser: bool = False
    boost: bool = True

    def get_url(self) -> str:
        try:
            return reverse(self.url)
        except NoReverseMatch:
            return self.url
