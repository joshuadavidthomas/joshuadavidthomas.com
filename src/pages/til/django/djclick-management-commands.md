---
layout: "../../../layouts/MarkdownLayout.astro"
title: "Using djclick for management commands"
description: "How I use the click cli package through djclick for better and more organized management commands in Django."
published: "2022-11-15"
tags: ["django", "click", "cli"]
---

```python
# app/management/commands/foo.py
from ...cli import *  # noqa: F401, F403
```

```python
# app/cli.py
import djclick as click


@click.group()
def cli():
    print("foo")


@cli.command()
def bar():
    print("bar")


@cli.command()
def baz():
    print("baz")
```

```shell
$ python -m manage foo
foo
$ python -m manage foo bar
foo
bar
$ python -m manage foo baz
foo
baz
```

