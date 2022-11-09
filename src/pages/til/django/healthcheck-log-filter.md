---
layout: "../../../layouts/MarkdownLayout.astro"
title: "Filtering Healthcheck Requests in Logs"
description: "This example shows how to filter healthcheck requests in logs."
published: "2022-01-17"
tags: ["django", "logging", "healthcheck"]
---

```py
# log_filters.py
import logging
import re

class HealthCheckFilter(logging.Filter):
    """
    A filter that discards requests to a healthcheck endpoint from
    certain health check user agents. This is useful to avoid
    unnecessary log spam from health checks.

    :param path_re: A regular expression that is used to match the request
        path.
    :param user_agents: A list of user agents that are used to make health
        check requests.
    """

    def __init__(self, *args, path_re: str, user_agents: list[str], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.path_filter = re.compile(path_re)
        self.user_agents_filter = user_agents

    def filter(self, record: logging.LogRecord) -> bool:
        req_path = record.args["U"]  # type: ignore
        user_agent = record.args["a"]  # type: ignore
        if not self.path_filter.match(req_path):
            return True
        if user_agent not in self.user_agents_filter:
            return True
        return False
```

```py
# settings.py
import os
import sys

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "filter_healthcheck_reqs": {
            "()": "log_filters.HealthCheckFilter",
            "path_re": r"^/up/$",
            "user_agents": [
                "docker/healthcheck",
                "Mozilla/5.0+(compatible; UptimeRobot/2.0; http://www.uptimerobot.com/)",
            ],
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "gunicorn.access": {
            "handlers": ["stdout"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "filters": ["filter_healthcheck_reqs"],
        },
    },
}
```
