---
layout: "../../../layouts/MarkdownLayout.astro"
title: "Monkeypatching imports correctly"
description: "TIL how to monkeypatch an import correctly"
published: "2022-11-15"
tags: ["pytest", "monkeypatch"]
--- 

```python
# twilio.py
from __future__ import annotations

from django.conf import settings

from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client


def get_twilio_client() -> Client:
    return Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        http_client=TwilioHttpClient(),
    )
```

```python
# conftest.py
from __future__ import annotations

from collections import namedtuple


@pytest.fixture
def mock_twilio_client(monkeypatch) -> None:
    class MockTwilioClient:
        def __init__(self, **kwargs):
            self.messages = self.MessageFactory()

        class MessageFactory:
            @staticmethod
            def create(**kwargs):
                Message = namedtuple("Message", ["sid"])

                return Message(sid="SM87105da94bff44b999e4e6eb90d8eb6a")

    def mock_get_twilio_client() -> MockTwilioClient:
        return MockTwilioClient()

    monkeypatch.setattr(
        "twilio.get_twilio_client", mock_get_twilio_client
    )
```

```python
# test_twilio.py
from __future__ import annotations

from .twilio import get_twilio_client


def test_monkeypatch_get_twilio_client(mock_twilio_client) -> None:
    client = get_twilio_client()

    message = client.messages.create(
        to="+1234567890",
        from_="+1234567891",
        body="Test message",
    )

    assert message.sid == "SM87105da94bff44b999e4e6eb90d8eb6a"
```

```python
from __future__ import annotations


def test_monkeypatch_get_twilio_client(mock_twilio_client):
    from .twilio import get_twilio_client

    client = get_twilio_client()

    message = client.messages.create(
        to="+1234567890",
        from_="+1234567891",
        body="Test message",
    )

    assert message.sid == "SM87105da94bff44b999e4e6eb90d8eb6a"
```
