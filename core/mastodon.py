from __future__ import annotations

import httpx
from django.conf import settings


def post_status_to_mastodon(message_html: str) -> int | None:
    try:
        response = httpx.post(
            f"{settings.MASTODON['URL'].rstrip('/')}/api/v1/statuses",
            headers={
                "Authorization": f"Bearer {settings.MASTODON['API_KEY']}",
            },
            data={
                "status": message_html,
            },
        )
        if response.status_code == 200:
            return response.json()["id"]
        else:
            return None
    except httpx.HTTPError:
        return None


def get_comments_on_status(status_id: int) -> list[dict[str, str]]:
    try:
        response = httpx.get(
            f"{settings.MASTODON['URL'].rstrip('/')}/api/v1/statuses/{status_id}/context",
            headers={
                "Authorization": f"Bearer {settings.MASTODON['API_KEY']}",
            },
        )
        if response.status_code == 200:
            return response.json()["descendants"]
        else:
            return []
    except httpx.HTTPError:
        return []
