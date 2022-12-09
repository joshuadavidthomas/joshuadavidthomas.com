---
layout: "../../../layouts/MarkdownLayout.astro"
title: "Leveraging `for_user` in a Custom Django Manager"
description: ""
published: "2022-12-09"
tags: ["django", "models", "managers"]
---

Back in July of this year, I had the pleasure of working with Frank Wiles of [REVSYS](https://revsys.com) on a code review of the Django application I have been working on at my [day job](https://westervelt.com). During the post-review discussion, Frank dropped a knowledge bomb on me that has been a game-changer for me and really helped me level up my Django skills.

I mentioned I found that dealing with permissions in Django and Django REST Framework slightly annoying and was wondering if there was a better way to handle it.

## Before

Here's a simplified example of what I was doing before, using the classic `Post`/`Author` example:

```python
# models.py
from django.auth import get_user_model
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
```

```python
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Post


@login_required
def my_view(request):
    posts = Post.objects.all()

    if not request.user.is_staff:
        posts = posts.filter(author=request.user)

    return render(request, "my_template.html", {"posts": posts})
```

In this view, only the staff should be able to see all posts, while regular users should only see their own posts. This is a pretty common use case, and I'm sure many of you have written something similar.

And it's honestly not bad! But as you can imagine as you add more views, more models, and more complex permissions, it can get a little unwieldy.

What happens when you need to update the permissions? You have to go through all of your views and update the logic, and you have to remember to do it everywhere. Automated tests are a great way to help with this and can really save your bacon, but: a) that's assuming you have a comprehensive test suite, and b) it's yet another place you have to remember to update the logic.

## After

The

```python
# models.py
from django.auth import get_user_model
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class PostManager(models.Manager):
    def for_user(self, user):
        queryset = self.get_queryset()

        if not user.is_staff:
            queryset = queryset.filter(author=user)

        return queryset


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)

    objects = PostManager()
```

```python
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Post


@login_required
def my_view(request):
    posts = Post.objects.for_user(request.user)

    return render(request, "my_template.html", {"posts": posts})
```

## Real-World Example

At work, we have an Onboarding application that helps with the onboarding process for new employees: what systems they need access to, any computer equipment they will need, etc. It was the first professional Django application I wrote, and while I'm proud of it, frankly it's a bit of a mess.

One area I didn't nail down till later was the new hire's hiring manager. It started out as a simple `ForeignKey` to a table containing all of the users in our Active Directory, but that meant I need to set up a sync process to keep that table up to date.

I also realized that with the `request` available in every view, I could just use the `request.user` to get the current user and set the hiring manager to that user. So I did that, and it worked great. However, the application had been in use for a while, and I needed a quick way to associate a new hire with their hiring manager going forward.

Thus, the `NewHire.hiring_manager2` field was born, set as a `ForeignKey` to my `User` model. Genius idea, right? 🙄 It was always meant as a temporary solution, until I could write a quick script to go through all of the existing new hires and consolidate the data. Spoiler alert: I never wrote that script.

Long story short, I ended up with views that looked like this:

```python
# views.py
from django.contrib.auth.decorators import login_required
from django.models import Q
from django.shortcuts import render

from .models import NewHire


@login_required
def dashboard(request):
    new_hires = NewHire.objects.all()

    if not request.user.is_staff:
        new_hires = new_hires.filter(
          Q(hiring_manager__mail=request.user.email) 
          | Q(hiring_manager2__email=request.user.email)
        )

    return render(
      request, "onboarding/dashboard.html", {"new_hires": new_hires}
    )
```

This type of logic was sprinkled *everywhere* in the application. It was a mess, and I knew it. Testing all of these views either wasn't done at all or was done manually. But I was too busy to fix it, and in the end it worked.

I recently had the opportunity to revisit the application and clean it up, and my first objective was to finally get rid of the multiple hiring manager fields. But before I could do that, I knew I need to centralize the logic for determining which new hires a user should be able to see.

```python
# models.py
from django.db import models


class NewHireManager(models.Manager):
    def for_user(self, user):
        queryset = self.get_queryset()

        if not user.is_staff:
            queryset = queryset.filter(
              Q(hiring_manager__mail=user.email) 
              | Q(hiring_manager2__email=user.email)
              # I also somehow ended up with an email field with manager's email
              # set, I think from a previous attempt at this
              | Q(old_hiring_manager_email=user.email)
            )

        return queryset


class NewHire(models.Model):
    ...
    hiring_manager = models.ForeignKey(
      "ADuser", on_delete=models.SET_NULL, null=True, related_name="new_hires"
    )
    hiring_manager2 = models.ForeignKey(
      "users.User", on_delete=models.SET_NULL, null=True, related_name="new_hires"
    )
    old_hiring_manager_email = models.EmailField(null=True, blank=True)
    ...

    objects = NewHireManager()
```

Now, I can just call `NewHire.objects.for_user(request.user)` anywhere in the application and know that I'm getting the correct new hires for that user. And I can write tests to ensure that the logic is correct.

And when I finally get around to consolidating the hiring manager fields, I'll only have to update the `NewHireManager` class, and I'll know that wherever I'm calling `NewHire.objects.for_user(request.user)`, I'm getting the correct new hires for that user.