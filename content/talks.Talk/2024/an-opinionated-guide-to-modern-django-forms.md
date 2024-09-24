---
title: An Opinionated Guide to Modern Django Forms
description: |
  TODO
stinger: So long, and thanks for all the fish!
---
{% load heroicons %}
{% load static %}
<!-- markdownlint-disable MD025 MD033 -->

<!-- .slide: class="title blue" -->
# What are forms? 📋

---

<!-- .slide: class="blue" -->
## `<form>`

---

<!-- .slide: class="title blue" -->
# What are forms? 📋

(in Django) <!-- .element class="fragment" role="doc-subtitle" -->

---

<!-- .slide: class="blue" -->
### Data Sanitation & Validation

### Presentation

---

<!-- .slide: class="blue" -->
## How long have forms been in Django?

---

<!-- .slide: class="blue" -->
<div class="flex-1 gap-8 mx-auto flex flex-col items-center justify-center">
  <h3><code>django/core/formfields.py</code></h3>
  <img src="{% static 'django-second-commit.png' %}" alt="Django's second public commit" class="min-w-full" />
  <ul class="!list-none !ml-0 space-y-8 !font-semibold !text-2xl">
    <li>
      <a href="https://github.com/django/django/commit/ed114e15106192b22ebb78ef5bf5bce72b419d13"
        class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
        {% heroicon_outline "link" class="size-6" %}
        https://github.com/django/django/commit/ed114e15106192b22ebb78ef5bf5bce72b419d13
      </a>
    </li>
    <li>
      <a href="https://github.com/django/django/blob/ed114e15106192b22ebb78ef5bf5bce72b419d13/django/core/formfields.py"
        class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
        {% heroicon_outline "link" class="size-6" %}
        https://github.com/django/django/blob/ed114e1...b419d13/django/core/formfields.py
      </a>
    </li>
  </ul>
</div>

---

<!-- .slide: class="blue" -->
| Version | Released | Notable changes to `django.forms`, according to release notes |
| --- | --- | --- |
| 0.95 | 2006-07-29 | First release available on GitHub, forms included |
| 0.96 | 2007-03-23 | `django.newforms` |
| 1.6 | 2013-11-06 | GeoDjango form widgets |
| 1.7 | 2014-09-02 | `Form.add_error()`, other validation changes |
| 1.11 | 2017-04-04 | Template-based widget rendering |
| 4.0 | 2021-12-07 | Template-based form rendering, `FormRenderer` |
| 4.1 | 2022-08-03 | `div`-based form templates, `FormRenderer.form_template_name` |
| 5.0 | 2023-12-04 | `as_field_group` |

---

<!-- .slide: class="blue" -->
![Django commit heatmap]({% static 'django_commits_heatmap.png' %}) <!-- .element class="" -->

---

<!-- .slide: class="blue" -->
![Django commit heatmap with forms highlighted]({% static 'django_commits_heatmap_forms_highlighted.png' %})

---

<!-- .slide: class="blue" -->
## What parts make up `django.forms`?

---

<!-- .slide: class="blue" -->
<dl class="space-y-4">
  <div>
    <dt>
      <code>Form</code>/<code>ModelForm</code>
    </dt>
    <dd>
      Central piece of puzzle, responsible for validation and rendering of all fields
    </dd>
  </div>
  <div>
    <dt>
      <code>FormSet</code>
    </dt>
    <dd>
      Multiple <code>Form</code> instances
    </dd>
  </div>
  <div>
    <dt>
      <code>Field</code>
    </dt>
    <dd>
      Responsible for validation and rendering of single field
    </dd>
  </div>
  <div>
    <dt>
      <code>Widget</code>
    </dt>
    <dd>
      Renders actual HTML input
    </dd>
  </div>
  <div>
    <dt>
      <code>BoundField</code>
    </dt>
    <dd>
      A combination of a field and data, either user created or initial
    </dd>
  </div>
  <div>
    <dt>
      <code>ErrorList</code>/<code>ErrorDict</code>
    </dt>
    <dd>
      Holds all errors from validation process
    </dd>
  </div>
</dl>

---

<!-- .slide: class="blue" -->
<figure>
  <img src="{% static 'pepe-silvia.gif' %}" alt="Charlie Day in It's Always Sunny in Philadephia" />
</figure>

<cite class="footnote">
  1. <a href="https://knowyourmeme.com/memes/pepe-silvia" class="!text-blue-50 hover:!text-blue-200">Pepe Silvia | Know Your Meme - https://knowyourmeme.com/memes/pepe-silvia</a>
</cite>

---

<!-- .slide: class="title emerald [&_h1]:!leading-[calc(var(--line-height)_*_0.55)]" -->
# Leveling up your `django.forms`

---

<!-- .slide: class="emerald" -->
<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto text-emerald-900">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center bg-white">
    ???
  </div>
  <img src="{% static 'levels-of-intelligence.png' %}" alt="Levels of Intelligence meme" class="-z-[1] !mx-auto absolute inset-0 !my-0 !h-full !max-h-full" />
</div>

---

<!-- .slide: class="emerald" -->
## Use the platform

---

<!-- .slide: class="emerald" -->
```html
<input type="number" />
<input type="email" />
<input type="url" />
<input type="password" />
```

---

<!-- .slide: class="emerald" -->
<iframe src="/talks/dcus2024/level1/"></iframe>

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.forms import widgets


class UseThePlatForm(forms.Form):
    number = forms.CharField(widget=widgets.NumberInput)
    email = forms.CharField(widget=widgets.EmailInput)
    url = forms.CharField(widget=widgets.URLInput)
    password = forms.CharField(widget=widgets.PasswordInput)
```

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.db import models


class UseThePlatformModel(models.Model):
    number = models.IntegerField(localize=False)  # otherwise `TextInput`
    email = models.EmailField()
    url = models.URLField()


class UseThePlatModelForm(forms.ModelForm):
    class Meta:
        model = UseThePlatformModel
        fields = "__all__"
```

---

<!-- .slide: class="emerald" -->
```html
<input type="color" />
<input type="search" />
<input type="tel" />
```

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.forms import widgets


class ColorInput(widgets.Input):
    input_type = "color"


class SearchInput(widgets.Input):
    input_type = "search"


class TelInput(widgets.Input):
    input_type = "tel"


class ComingInDjango52Form(forms.Form):
    color = forms.CharField(widget=ColorInput)
    search = forms.CharField(widget=SearchInput)
    tel = forms.CharField(widget=TelInput)
```

---

<!-- .slide: class="emerald" -->
<iframe src="/talks/dcus2024/django52/"></iframe>

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.forms import widgets


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateForm(forms.Form):
    date = forms.DateField(widget=DateInput)
    datetime = forms.DateTimeField(widget=DateTimeInput)
```

---

<!-- .slide: class="emerald" -->
<iframe src="/talks/dcus2024/date/"></iframe>

---

<!-- .slide: class="emerald" -->
## `has`

---

<!-- .slide: class="emerald" -->
<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto text-emerald-900">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <p>Use the platform</p>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center bg-white">
    ???
  </div>
  <img src="{% static 'levels-of-intelligence.png' %}" alt="Levels of Intelligence meme" class="-z-[1] !mx-auto absolute inset-0 !my-0 !h-full !max-h-full" />
</div>

---

<!-- .slide: class="emerald" -->
## `field.as_field_group`

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.forms.renderers import TemplatesSetting


class AsFieldGroupForm(forms.Form):
    has_custom_template = forms.CharField(template_name="custom_template.html")


def index(request):
    form = AsFieldGroupForm()
    has_custom_template = form["has_custom_template"]
    context = {
        "has_custom_template": has_custom_template.render(
            "different_custom_template.html"
        )
    }
    return render(request, "index.html", context)


class MyPreciousFormRenderer(TemplatesSetting):
    field_template_name = "custom_field_template_to_rule_them_all.html"
```

---

<!-- .slide: class="emerald" -->
{% verbatim %}

```html
<form class="grid grid-cols-1 gap-4">
  {{ form.non_field_errors }}
  <div>
    {{ form.has_custom_template.as_field_group }}
  </div>
</form>
```

{% endverbatim %}

---

<!-- .slide: class="emerald" -->
<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto text-emerald-900">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <p>Use the platform</p>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <code>
      field.as_field_group
    </code>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    ???
  </div>
  <div class="col-start-1 flex items-center justify-center bg-white">
    ???
  </div>
  <img src="{% static 'levels-of-intelligence.png' %}" alt="Levels of Intelligence meme" class="-z-[1] !mx-auto absolute inset-0 !my-0 !h-full !max-h-full" />
</div>

---

<!-- .slide: class="emerald" -->
## `FormRenderer`

---

<!-- .slide: class="emerald" -->
```python
from django import forms
from django.forms.renderers import TemplatesSetting


class FormRendererForm(forms.Form):
    template_name = "custom_form_template.html"


def index(request):
    form = FormRendererForm()
    rendered_form = form.render("different_custom_form_template.html")
    context = {"form": rendered_form}
    return render(request, "index.html", context)


class MyPreciousFormRenderer(TemplatesSetting):
    form_template_name = "custom_form_template_to_rule_them_all.html"
```

---

<!-- .slide: class="emerald" -->
```python
# settings.py
from django import forms


class MyPreciousFormRenderer(TemplatesSetting):
    form_template_name = "custom_form_template_to_rule_them_all.html"


FORM_RENDERER = "settings.MyPreciousFormRenderer"
```

---

<!-- .slide: class="emerald" -->
<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto text-emerald-900">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <p>Use the platform</p>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <code>
      field.as_field_group
    </code>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <code>
      FormRenderer
    </code>
  </div>
  <div class="col-start-1 flex items-center justify-center bg-white">
    ???
  </div>
  <img src="{% static 'levels-of-intelligence.png' %}" alt="Levels of Intelligence meme" class="-z-[1] !mx-auto absolute inset-0 !my-0 !h-full !max-h-full" />
</div>

---

<!-- .slide: class="emerald" -->
## Maybe don't use `django.forms`?

---

<!-- .slide: class="emerald" -->
## Maybe don't use `django.forms` only?

---

<!-- .slide: class="emerald" -->
<ul>
  <li>
    Form specific
    <ul class="!list-none">
      <li>
        <a href="https://github.com/django-crispy-forms/django-crispy-forms"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          django-crispy-forms/django-crispy-forms
        </a>
      </li>
      <li>
        <a href="https://github.com/jazzband/django-widget-tweaks"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          jazzband/django-widget-tweaks
        </a>
      </li>
      <li>
        <a href="https://github.com/jrief/django-formset"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          jrief/django-formset
        </a>
      </li>
    </ul>
  </li>
  <li>
    Template-based components
    <ul class="!list-none">
      <li>
        <a href="https://github.com/carltongibson/django-template-partials"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          carltongibson/django-template-partials
        </a>
      </li>
      <li>
        <a href="https://github.com/EmilStenstrom/django-components"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          EmilStenstrom/django-components
        </a>
      </li>
      <li>
        <a href="https://github.com/mixxorz/slippers"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          mixxorz/slippers
        </a>
      </li>
      <li>
        <a href="https://github.com/wrabit/django-cotton"
          class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
          <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
            <title>GitHub</title>
            <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
            </path>
          </svg>
          wrabit/django-cotton
        </a>
      </li>
    </ul>
  </li>
</ul>

---

<!-- .slide: class="emerald" -->
{% verbatim %}

```html
<!-- cotton/input.html -->
<c-vars type="text" leading_icon trailing_icon />

<div class="border rounded shadow flex items-center">
    {% if leading_icon %}
        <div class="pl-3">{{ leading_icon }}</div>
    {% endif %}

    <input type="{{ type }}" {{ attrs }} class="px-3 py-1.5 w-full">
</div>

<!-- form_template.html -->
<c-input type="password" name="password" name="password" placeholder="Password">
    <c-slot name="leading_icon">
        <svg>...</svg>
    </c-slot>
</c-input>
```

{% endverbatim %}

![Cotton input with leading icon]({% static 'cotton-input.png' %}) <!-- .element: class="!max-w-[33.3%] !my-0" -->

---

<!-- .slide: class="emerald" -->
<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto text-emerald-900">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <p>Use the platform</p>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <code>
      field.as_field_group
    </code>
  </div>
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    <code>
      FormRenderer
    </code>
  </div>
  <div class="col-start-1 flex items-center justify-center bg-white">
    <p>Maybe don't use <code>django.forms</code> only?</p>
  </div>
  <img src="{% static 'levels-of-intelligence.png' %}" alt="Levels of Intelligence meme" class="-z-[1] !mx-auto absolute inset-0 !my-0 !h-full !max-h-full" />
</div>

---

<!--- .slide: class="title orange" -->
# Let's build! 👷💪

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/8/"></iframe>

---

<!--- .slide: class="bg-red-600 text-red-50" -->
## 🚨 Disclaimer 🚨

**Do *NOT* use this in a production application!**

---

<!-- .slide: class="orange" -->
```python
from django import forms
from django.views.generic import FormView


class PasswordResetForm(forms.Form):
    current_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()


class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = "password_reset_form.html"
```

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_reset_form.html -->
<form>
  {{ form }}
  <button type="submit">Submit</button>
</form>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/1/"></iframe>

---

<!-- .slide: class="orange" -->
```python
from django import forms
from django.views.generic import FormView


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)


class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = "password_reset_form.html"
```

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/2/"></iframe>

---

<!-- .slide: class="orange" -->
```python
from django import forms


class PasswordField(forms.CharField):
    widget = forms.PasswordInput

    def __init__(self, *args, **kwargs):
        if kwargs.get("template_name") is None:
            kwargs["template_name"] = "password_field.html"
        super().__init__(*args, **kwargs)


class PasswordResetForm(forms.Form): ...
```

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_field.html -->
{% if field.label %}
  <label for="{{ field.auto_id }}"
         class="mb-2 block text-sm font-medium select-none text-gray-900 cursor-default">
    {{ field.label }}
  </label>
{% endif %}

{% if field.errors %}
  <div class="text-red-500 text-xs mt-2 ">{{ field.errors }}</div>
{% endif %}

{{ field }}

{% if field.help_text %}
  <p {% if field.auto_id %}id="{{ field.auto_id }}_helptext"{% endif %}>
    {{ field.help_text|safe }}
  </p>
{% endif %}
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
```python
from django import forms


class PasswordField(forms.CharField): ...


class PasswordResetForm(forms.Form):
    current_password = PasswordField()
    new_password1 = PasswordField()
    new_password2 = PasswordField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full border rounded-lg text-sm h-10 leading-6 px-3 bg-white"
                    "text-gray-700 placeholder-gray-400 shadow-sm border-gray-300"
                    "border-b-gray-400/80 focus:border-blue-500",
                }
            )
```

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_reset_form.html -->
<div class="flex items-center justify-center min-h-full">
  <form class="grid grid-cols-1 gap-4">
    {{ form }}
    <button type="submit"
            class="mt-4 h-10 text-blue-50 font-medium text-sm px-4 bg-blue-800
                                hover:bg-blue-900 rounded-lg whitespace-nowrap flex items-center
                                justify-center shadow-[inset_0px_1px_theme(colors.blue.900)]
                                active:scale-[.99] focus:outline-2 focus:outline-offset-[3px]
                                focus:outline focus:outline-blue-500">
      Submit
    </button>
  </form>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/3/"></iframe>

---

<!-- .slide: class="orange" -->
```python
from django import forms


class PasswordField(forms.CharField): ...


class PasswordResetForm(forms.Form):
    current_password = ...
    new_password1 = PasswordField(label="")
    new_password2 = PasswordField(label="")

    def __init__(self, *args, **kwargs): ...
```

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_reset_form.html -->
<div class="flex items-center justify-center min-h-full">
  <form class="grid grid-cols-1 gap-4">
    {{ form.non_field_errors }}

    <div>{{ form.current_password.as_field_group }}</div>

    <fieldset>
      <legend class="mb-2 block text-sm font-medium
                                   select-none text-gray-900 cursor-default">
        New password
      </legend>
      <div class="grid grid-cols-1 gap-2">
        <div>{{ form.new_password1.as_field_group }}</div>
        <div>{{ form.new_password2.as_field_group }}</div>
      </div>
    </fieldset>

    <button>...</button>
  </form>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/4/"></iframe>

---

<!-- .slide: class="orange" -->
```python
from django import forms


class PasswordField(forms.CharField): ...


class PasswordResetForm(forms.Form):
    ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.template_name = "password_input.html"
```

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_input.html -->
<div class="grid grid-cols-[theme(spacing.10)_1fr_theme(spacing.10)]"
     id="{{ widget.attrs.id }}_container"
     x-data="{ hidden: true }">
  ...
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_input.html -->
<div ...>

  <input :type="hidden ? 'password' : 'text'"
         name="{{ widget.name }}"
         class="col-span-3 col-start-1 row-start-1 w-full border pr-8 rounded-lg text-sm
                              h-10 leading-6 px-3 bg-white text-gray-700 placeholder-gray-400 shadow-sm
                              border-gray-300 border-b-gray-400/80 focus:border-blue-500"
         {% if widget.value != None %}
           value="{{ widget.value|stringformat:'s' }}"
         {% endif %}
         {% include "django/forms/widgets/attrs.html" %}>

    ...
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_input.html -->
{% load heroicons %}

<div ...>
  <input ...>

  <button type="button"
          id="{{ widget.attrs.id }}_toggle"
          class="flex items-center justify-center w-full h-full place-self-center
                               text-gray-400 hover:text-gray-700 focus:text-gray-700 col-start-3
                               row-start-1 z-10 rounded-r-lg focus:outline focus:outline-2
                               focus:outline-blue-500"
          @click="hidden = !hidden">
    {% heroicon_outline "eye-slash" class="size-4" x_show="hidden" %}
    {% heroicon_outline "eye" class="size-4" x_show="!hidden" %}
  </button>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_input.html -->
{% load heroicons %}

<div class="grid grid-cols-[theme(spacing.10)_1fr_theme(spacing.10)]"
     id="{{ widget.attrs.id }}_container"
     x-data="{ hidden: true }">

  <input :type="hidden ? 'password' : 'text'"
         name="{{ widget.name }}"
         class="col-span-3 col-start-1 row-start-1 w-full border pr-8 rounded-lg text-sm h-10 leading-6 px-3 bg-white text-gray-700 placeholder-gray-400 shadow-sm border-gray-300 border-b-gray-400/80 focus:border-blue-500"
         {% if widget.value != None %}value="{{ widget.value|stringformat:'s' }}"{% endif %}
         {% include "django/forms/widgets/attrs.html" %}>

  <button type="button"
          id="{{ widget.attrs.id }}_toggle"
          class="flex items-center justify-center w-full h-full place-self-center text-gray-400 hover:text-gray-700 focus:text-gray-700 col-start-3 row-start-1 z-10 rounded-r-lg focus:outline focus:outline-2 focus:outline-blue-500"
          @click="hidden = !hidden">
    {% heroicon_outline "eye-slash" class="size-4" x_show="hidden" %}
    {% heroicon_outline "eye" class="size-4" x_show="!hidden" %}
  </button>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/5/"></iframe>

---

<!-- .slide: class="orange" -->
<a href="https://github.com/spookylukey/django-htmx-patterns"
  class="flex items-center gap-4 !text-blue-50 hover:!text-blue-200">
  <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="size-12">
    <title>GitHub</title>
    <path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.083-.202-.358-1.015.077-2.117 0 0 .672-.215 2.2.82.638-.178 1.323-.266 2.003-.27.68.004 1.364.092 2.003.27 1.527-1.035 2.198-.82 2.198-.82.437 1.102.163 1.915.08 2.117.513.56.823 1.274.823 2.147 0 3.073-1.87 3.75-3.653 3.947.287.246.543.735.543 1.48 0 1.07-.01 1.933-.01 2.195 0 .215.144.463.55.385C13.71 14.53 16 11.534 16 8c0-4.418-3.582-8-8-8">
    </path>
  </svg>
  spookylukey/django-htmx-patterns
</a>

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_reset_form.html -->
{% load partials %}

{% partialdef field-partial %}
  <div hx-get="."
       hx-vals='{"_validate_field": "{{ field.name }}" }'
       hx-trigger="password-blur from:#{{ field.auto_id }}_container"
       hx-include="#{{ field.auto_id }}"
       hx-target="this"
       hx-ext="morph"
       hx-swap="morph:outerHTML">
    {{ field.as_field_group }}
  </div>
{% endpartialdef %}

<div class="flex items-center justify-center min-h-full">
  <form class="grid grid-cols-1 gap-4">
    ...
  </form>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<div class="flex items-center justify-center min-h-full">
  <form class="grid grid-cols-1 gap-4">
    {{ form.non_field_errors }}
    {% with field=form.current_password %}
      {% partial field-partial %}
    {% endwith %}
    <fieldset>
      <legend class="mb-2 block text-sm font-medium text-gray-900 cursor-default">
        New password
      </legend>
      <div class="grid grid-cols-1 gap-2">
        {% with field=form.new_password1 %}
          {% partial field-partial %}
        {% endwith %}
        {% with field=form.new_password2 %}
          {% partial field-partial %}
        {% endwith %}
      </div>
    </fieldset>
    <button>...</button>
  </form>
</div>
```

{% endverbatim %}

---

<!-- .slide: class="orange" -->
{% verbatim %}

```html
<!-- password_input.html -->
<div ...
     x-data="{
        hidden: true,
        hasFocus: false,
        handleFocusLoss() {
          if (!this.hasFocus) {
            this.$dispatch('password-blur');
          }
        }
      }">
  <input ...
         x-on:focus="hasFocus = true"
         x-on:blur="hasFocus = false; $nextTick(() => handleFocusLoss())">
  <button ...
          x-on:focus="hasFocus = true"
          x-on:blur="hasFocus = false; $nextTick(() => handleFocusLoss())">
    ...
  </button>
</div>
```

{% endverbatim %}
---

<!-- .slide: class="orange" -->
```python
from django.views.generic import FormView


class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = "password_reset_form.html"
```

---

<!-- .slide: class="orange" -->
```python
class PasswordResetFormView(FormView):
    ...

    def get(self, request, *args, **kwargs):
        if request.htmx and (
            htmx_validation_field := request.GET.get("_validate_field", None)
        ):
            form = self.form_class(request.GET)
            form.is_valid()
            bound_field = form[htmx_validation_field]
            rendered = form.render(
                context={
                    "field": bound_field,
                    "errors": form.error_class(
                        bound_field.errors, renderer=form.renderer
                    ),
                },
                template_name=f"{self.template_name}#field-partial",
            )
            return HttpResponse(rendered)
        return super().get(request, *args, **kwargs)
```

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/6/"></iframe>

---

<!-- .slide: class="orange" -->
```python
class PasswordResetForm(forms.Form):
    ...

    def __init__(self, *args, **kwargs): ...

    def clean_current_password(self):
        data = self.cleaned_data["current_password"]
        if data != "dcus2024":
            raise forms.ValidationError("Does not match current password")
        return data
```

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/7/"></iframe>

---

<!-- .slide: class="orange" -->
```python
from django.contrib.auth import password_validation


class PasswordResetForm(forms.Form):
    current_password = ...
    new_password1 = PasswordField(
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = ...

    def __init__(self, *args, **kwargs): ...

    def clean_current_password(self): ...

    def clean_new_password1(self):
        new_password1 = self.cleaned_data["new_password1"]
        password_validation.validate_password(new_password1)
        return new_password1
```

---

<!-- .slide: class="orange" -->
<iframe src="/talks/dcus2024/password-reset/8/"></iframe>
