from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
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


class CustomRenderer(RendererHTML):
    def fence(self, tokens, idx, options, env):
        ret = super().fence(tokens, idx, options, env)
        # pre_tag = "<pre>"
        # pre_class_tag = "<pre class='not-prose stretch-to-5xl'>"
        # if pre_tag in ret:
        #     # Find the first occurrence and replace it
        #     pos = ret.find(pre_tag)
        #     ret = ret[:pos] + pre_class_tag + ret[pos + len(pre_tag) :]
        return f"<div class='not-prose stretch-to-5xl'>{ret}</div>"


md = (
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
