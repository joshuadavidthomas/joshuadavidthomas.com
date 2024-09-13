from __future__ import annotations

import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def highlight_code(code, name, attrs):
    lexer = get_lexer_by_name(name)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)


md = (
    MarkdownIt(
        "commonmark",
        {"html": True, "highlight": highlight_code},
    )
    .use(admon_plugin)
    .use(
        anchors_plugin,
        max_level=4,
        permalink=True,
        permalinkSymbol="#",
    )
    .use(footnote_plugin)
    .use(front_matter_plugin)
    .enable(["table"])
)


class Markdown:
    def __init__(self, raw_markdown: str) -> None:
        self.raw_markdown = raw_markdown

    def get_frontmatter_token(self) -> dict[str, str]:
        parsed_markdown = self.mdit.parse(self.raw_markdown)
        fm_tokens = [token for token in parsed_markdown if token.type == "front_matter"]
        if len(fm_tokens) == 0:
            return {}
        if len(fm_tokens) > 1:
            raise ValueError("Multiple frontmatter blocks found")
        return fm_tokens[0]

    def get_frontmatter(self) -> dict[str, str]:
        fm_token = self.get_frontmatter_token()
        return yaml.safe_load(fm_token.content)

    def render_plain(self) -> str:
        lines = self.raw_markdown.splitlines()
        fm_token = self.get_frontmatter_token()
        if fm_token:
            lines = lines[fm_token.map[1] :]
        lines = [line for line in lines if line.strip()]
        return "\n\n".join(lines)

    def render_html(self, trailing_newline: bool = True) -> str:
        rendered = self.mdit.render(self.raw_markdown)
        if trailing_newline:
            rendered = rendered.lstrip()
        else:
            rendered = rendered.strip()
        return rendered

    @property
    def mdit(self) -> MarkdownIt:
        return (
            MarkdownIt(
                "commonmark",
                {"html": True, "highlight": highlight_code},
                renderer_cls=CustomRenderer,
            )
            .use(admon_plugin)
            .use(
                anchors_plugin,
                max_level=4,
                permalink=True,
                permalinkSymbol="#",
            )
            .use(footnote_plugin)
            .use(front_matter_plugin)
            .enable(["table"])
        )
