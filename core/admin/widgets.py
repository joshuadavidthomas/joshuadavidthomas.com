from __future__ import annotations

from django import forms
from django.utils.html import html_safe
from django_vite.core.asset_loader import DjangoViteAssetLoader


@html_safe
class EasyMDEJSCDN:
    def __str__(self):
        return '<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>'


@html_safe
class EasyMDECSSCDN:
    def __str__(self):
        return '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css">'


class EasyMDEWidget(forms.Widget):
    class Media:
        js = [EasyMDEJSCDN()]
        css = {"all": [EasyMDECSSCDN()]}

    template_name = "widgets/easymde_widget.html"

    def __init__(self, attrs=None, width=None, height=None):
        self.width = width
        self.height = height

        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context["widget"]["width"] = self.width
        context["widget"]["height"] = self.height

        return context


@html_safe
class TipTapWebComponent:
    def __str__(self):
        return """
<script type="module">
class TipTapEditor extends HTMLElement {
  constructor() {
    super(); // Always call super first in constructor
    this.attachShadow({ mode: 'open' }); // Attach a shadow root to the element.
  }

  connectedCallback() {
    const editorContainer = document.createElement('div');
    this.shadowRoot.appendChild(editorContainer);

    const initialValue = this.innerHTML.trim();
    this.innerHTML = ''; // Clear the inner HTML as it's no longer needed
    console.log(initialValue);

    import('https://esm.sh/@tiptap/core@2.1.14').then(({ Editor }) => {
      import('https://esm.sh/@tiptap/starter-kit@2.1.14').then(({ default: StarterKit }) => {
        new Editor({
          element: editorContainer,
          extensions: [
          StarterKit.configure({
            heading: {
              HTMLAttributes: {
                class: 'my-custom-heading',
              },
            },
          }),
        ],
        editorProps: {
          attributes: {
            class: 'prose dark:prose-invert prose-sm sm:prose-base lg:prose-lg xl:prose-2xl m-5 focus:outline-none',
          },
        },
        content: initialValue || '<p>Hello, World!</p>',
        });
      });
    });
  }
}
customElements.define('tiptap-editor', TipTapEditor);
</script>
"""


@html_safe
class TipTapSvelteComponent:
    def __str__(self):
        return DjangoViteAssetLoader.instance().generate_vite_asset("tiptap.ts")


class TipTapWidget(forms.Widget):
    class Media:
        # js = [TipTapWebComponent()]
        # js = [DjangoViteAssetLoader.instance().generate_vite_asset("tiptap.js")]
        js = [TipTapSvelteComponent()]

    template_name = "widgets/tiptap_widget.html"
