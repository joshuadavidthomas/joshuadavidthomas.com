from __future__ import annotations

from markdown_it import MarkdownIt
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class NotProseHtmlFormatter(HtmlFormatter):
    # this wraps the code in a div twice, which is not ideal
    # but works for now
    def wrap(self, source):
        wrapped = super().wrap(source)
        return self._wrap_div(wrapped)

    def _wrap_div(self, wrapped):
        yield 0, '<div class="not-prose my-2">'
        for item in wrapped:
            yield item
        yield 0, "</div>"


def highlight_code(code, name, attrs):
    lexer = get_lexer_by_name(name)
    formatter = NotProseHtmlFormatter()
    return highlight(code, lexer, formatter)


md = (
    MarkdownIt("commonmark", {"html": True, "highlight": highlight_code})
    .use(admon_plugin)
    .use(anchors_plugin)
    .use(footnote_plugin)
    .use(front_matter_plugin)
    .enable(["table"])
)
