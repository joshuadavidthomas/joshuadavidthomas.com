---
title: An Opinionated Guide to Modern Django Forms
description: |
  In my journey as a Django developer, I know the moment when I did not consider myself a
  beginner anymore: when I started leveraging Django custom model managers and querysets.
  Initially they can seem intimidating and potentially complex. However, they can help
  make your use of the ORM more efficient, allow you to encapsulate complex and repetitive
  queries, and provide an API surface area that makes it easier to introduce certain changes
  to Model fields and queries, among other benefits.
stinger: So long, and thanks for all the fish!
---
{% load static %}
<!-- markdownlint-disable MD025 MD033 -->
<!-- .slide: class="title blue" -->

# What are forms? 📋

(in Django) <!-- .element class="fragment" role="doc-subtitle" -->

---

## `<form>`

---

## `django.forms.Form`

---

### Validation

### Presentation

---

<dl>
  <dt>
    <code>Form</code>/<code>ModelForm</code>
  </dt>
  <dt>
    <code>Field</code>
  </dt>
  <dt>
    <code>Widget</code>
  </dt>
  <dt>
    <code>BoundField</code>
  </dt>
</dl>

---

```mermaid
classDiagram
Form <|-- ModelForm
Form *-- Field
Form *-- BoundField
Form *-- Renderer
Form *-- ErrorDict
Form -- Validation
Field *-- Widget
BoundField *-- Field
BoundField *-- ErrorList
FormSet *-- Form
ErrorDict *-- ErrorList

class Form {
+fields
+clean()
+is_valid()
+render()
}

class ModelForm {
+model
+save()
}

class Field {
+widget
+validators
+clean()
}

class Widget {
+render()
}

class BoundField {
+field
+form
+render()
}

class FormSet {
+forms
+is_valid()
}

class Renderer {
+render()
}

class Validation {
+validate()
}

class ErrorDict {
+errors
}

class ErrorList {
+errors
}
```

---

<figure>
  <img src="{% static 'pepe-silvia.gif' %}" alt="Charlie Day in It's Always Sunny in Philadephia" />
  <figcaption>
    Charlie Day as Charlie in <i>It's Always Sunny in Philadephia</i>, "Sweet Dee Has a Heart Attack"<sup>1</sup>
  </figcaption>
</figure>

<cite class="footnote">
  1. <a href="https://knowyourmeme.com/memes/pepe-silvia">Pepe Silvia | Know Your Meme - https://knowyourmeme.com/memes/pepe-silvia</a>
</cite>

---

<iframe src="/talks/dcus2024/level1/"></iframe>

---

<iframe src="/talks/dcus2024/date/"></iframe>

---

<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto">
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

## Use the platform

---

<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    Use the platform
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

## `field.as_field_group`

---

<div class="isolate relative font-brico text-4xl font-semibold grid grid-rows-4 grid-cols-2 h-full w-5/6 mx-auto">
  <div class="col-start-1 flex items-center justify-center border-b-8 border-gray-900 bg-white">
    Use the platform
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

<!--- .slide: class="title orange" -->
# Let's build! 👷💪

---

<!--- .slide: class="bg-orange-600 text-orange-50" -->
## Scenario

---

<h3>Choose your PM</h3>
<div class="relative grid grid-cols-1 md:grid-cols-2 gap-8 px-4 w-full h-full text-7xl md:text-9xl" x-data="{ clickCount: 0 }">
  <button type="button" class="flex flex-col items-center justify-center border-green-500 border-2 shadow-lg bg-green-500/10 hover:bg-green-500/75 rounded-lg" @click="clickCount++">
    <img src="{% static 'guinan-1.jpg' %}" alt="Guinan" class="w-full" x-show="clickCount < 10"/>
    <img src="{% static 'guinan-2.jpg' %}" alt="Guinan" class="w-full -scale-x-[1]" x-show="clickCount >= 10 && clickCount < 20"/>
    <img src="{% static 'guinan-3.jpg' %}" alt="Guinan" class="w-full -scale-x-[1]" x-show="clickCount >= 20 && clickCount < 30"/>
    <p class="font-brico font-semibold">Guinan</p>
  </button>
  <button type="button" class="flex flex-col items-center justify-center border-red-500 border-2 shadow-lg bg-red-500/10 hover:bg-red-500/75 rounded-md" @click="Reveal.right()">
    <img src="{% static 'q-1.jpg' %}" alt="Q" class="w-full -scale-x-[1]" x-show="clickCount < 10"/>
    <img src="{% static 'q-2.jpg' %}" alt="Q" class="w-full" x-show="clickCount >= 10 && clickCount < 20"/>
    <img src="{% static 'q-3.jpg' %}" alt="Q" class="w-full" x-show="clickCount >= 20 && clickCount < 30"/>
    <p class="font-brico font-semibold">Q</p>
  </button>
  <div class="fixed right-2 top-2 text-xs font-medium">
    Click count: <span x-text="clickCount"></span>
  </div>
  <template x-if="clickCount > 1">
    <div class="z-10 bg-gray-900/75 fixed inset-0 flex items-center justify-center">
      <div class="uppercase fixed inset-0 z-10 flex items-center justify-center flex-col text-8xl font-medium">
        <p>Captain Jean-Luc Picard</p>
        <p>USS Enterprise</p>
      </div>
      <img src="{% static 'picard-ytmnd.jpg' %}" alt="Captain Jean Luc Picard of the USS Enterprise" class="h-full col-start-1" />
      <audio src="{% static 'captain-jean-luc.wav' %}" loop autoplay></audio>
    </div>
  </template>
</div>

---

<iframe src="/talks/dcus2024/password-reset/"></iframe>
