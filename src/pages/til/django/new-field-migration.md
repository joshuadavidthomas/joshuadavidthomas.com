---
layout: "../../../layouts/MarkdownLayout.astro"
title: "New/Changed Fields in Migrations"
description: "How I safely deal with new or changed fields and any associated data in Django migrations."
published: "2022-11-21"
tags: ["django", "migrations"]
---

Recently I wanted to change a model from using a Choice field provided by
`django-model-utils` to finite state machine provided by `django-fsm`. I
wanted to do this in a way that preserved the existing data in the database
and made it easy to add new states in the future.

For reference, here is a simplified version of the model and associated
methods I was using before the change:

```python
# models.py
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel


class Import(StatusModel):
    STATUS = Choices("uploaded", "processing", "error", "complete")

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            self.process()

    def set_status(self, status: str):
        self.status = status
        self.save()

    def process(self):
        self.set_status(self.STATUS.processing)
        try:
            # do some processing
        except Exception:
            # handle error by sending notifications, etc...
            self.set_status(self.STATUS.error)

        self.set_status(self.STATUS.complete)
```

Pretty simple, right? The `StatusModel` class provides a `status` field
that is a `CharField` with a `choices` argument derived from the `STATUS`
constant (the first choice being the default value). The `save` method is
overridden to call `process` when the model is first created. The
`process` method is responsible for doing the actual work of the import and
handling the various statuses.

Having recently read about Finite State Machines (FSM) and how they can be
used to model processes just like this, I decided to give it a try with
the popular `django-fsm` package.

First, the steps required to migrate the model. After installing the package,
I added a `status_state` `django_fsm.FSMField` field to the model with the 
requisite `TextChoices` to define the states:

```python
# models.py
from django.db import models
from django_fsm import FSMField
from model_utils import Choices
from model_utils.models import StatusModel


class Import(StatusModel):
    STATUS = Choices("uploaded", "processing", "error", "complete")

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        ERROR = "ERROR", "Error"
        COMPLETE = "COMPLETE", "Complete"

    status_state = FSMField(choices=Status.choices, default=Status.UPLOADED)
    ...
```

Next, I added the required transition methods to the model, decorated with
`django_fsm.transition` to define the transitions between states:

```python
# models.py
from django.db import models
from django_fsm import FSMField
from django_fsm import transition
from model_utils import Choices
from model_utils.models import StatusModel


class Import(StatusModel):
    STATUS = Choices("uploaded", "processing", "error", "complete")

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        ERROR = "ERROR", "Error"
        COMPLETE = "COMPLETE", "Complete"

    status_state = FSMField(choices=Status.choices, default=Status.UPLOADED)

    @transition(field=status_state, source=Status.UPLOADED, target=Status.PROCESSING)
    def process(self):
        try:
            # do some processing
            ...
        except Exception:
            self.handle_error()

    @transition(field=status_state, source=[Status.UPLOADED, Status.PROCESSING], target=Status.ERROR)
    def handle_error(self):
        # handle error by sending notifications, etc...
        ...

    @transition(field=status_state, source=Status.PROCESSING, target=Status.COMPLETE)
    def mark_complete(self):
        # do any cleanup, send success notifications, etc...
        ...
    
    ...
```

Finally, I modified the `save` method to call these new transition methods and
deleted the unnecessary `set_status` method:

```python
# models.py
from django.db import models
from django_fsm import FSMField
from django_fsm import transition
from model_utils import Choices
from model_utils.models import StatusModel


class Import(StatusModel):
    STATUS = Choices("uploaded", "processing", "error", "complete")

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        ERROR = "ERROR", "Error"
        COMPLETE = "COMPLETE", "Complete"

    status_state = FSMField(choices=Status.choices, default=Status.UPLOADED)

    @transition(field=status_state, source=Status.UPLOADED, target=Status.PROCESSING)
    def process(self):
        try:
            # do some processing
            ...
        except Exception:
            self.handle_error()

    @transition(field=status_state, source=[Status.UPLOADED, Status.PROCESSING], target=Status.ERROR)
    def handle_error(self):
        # handle error by sending notifications, etc...
        ...

    @transition(field=status_state, source=Status.PROCESSING, target=Status.COMPLETE)
    def mark_complete(self):
        # do any cleanup, send success notifications, etc...
        ...

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            self.process()
```

With all of that in place, I was ready to generate the migration. I ran
`python manage.py makemigrations` and got the following auto-generated
migration:

```python
# migrations/xxxx_random_migration_name.py
from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', 'xxxx_previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='status_state',
            field=django_fsm.FSMField(choices=[('UPLOADED', 'Uploaded'), ('PROCESSING', 'Processing'), ('ERROR', 'Error'), ('COMPLETE', 'Complete')], default='UPLOADED', max_length=50),
        ),
    ]
```

In order to ensure the data is migrated correctly, I needed to add a 
`migrations.RunPython` operation after the `AddField` operation, along with
two `forward_func` and `reverse_func` functions, to handle the migration:

```python
# migrations/xxxx_random_migration_name.py
from django.db import migrations
import django_fsm


def forward_func(apps, schema_editor):
    ...

def reverse_func(apps, schema_editor):
    ...

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', 'xxxx_previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='status_state',
            field=django_fsm.FSMField(choices=[('UPLOADED', 'Uploaded'), ('PROCESSING', 'Processing'), ('ERROR', 'Error'), ('COMPLETE', 'Complete')], default='UPLOADED', max_length=50),
        ),
        migrations.RunPython(forward_func, reverse_func),
    ]
```

The `forward_func` function would be responsible for migrating the data from
the `status` field to the new `status_state` field. The `reverse_func` would
be responsible for migrating the data back from the `status_state` field to
the `status` field, though in this case, I didn't need to worry about that
since on reverting the migration, the `status_state` field would be deleted anyway.

```python
# migrations/xxxx_random_migration_name.py
from django.db import migrations
import django_fsm


def forward_func(apps, schema_editor):
    Import = apps.get_model("myapp", "Import")
    
    imports = Import.objects.all()

    for import_ in imports:
        import_.status_state = import_.status.upper()

    Import.objects.bulk_update(imports, ["status_state"])

def reverse_func(apps, schema_editor):
    ...

...
```

I used the `bulk_update` method to update all of the `Import` objects in a
single query. I also needed to convert the `status` field value to uppercase
to match the `status_state` field values.

Finally, I ran `python manage.py migrate` to apply the migration, checked the
data in my local development database, and verified that the data was
migrated correctly.

After that, I was able to remove the `StatusModel` class from my `Import`
model and the `status` field. I also set `protected=True` on the
`status_state` field (doing so before the migration would have resulted in
migration errors), and renamed the `status_state` field to `status` for
good measure. These last two changes needed to be done in two separate
migrations (Django tried to drop the `status_state` field instead of renaming
due to some ORM magic I assume).

The final `Import` model resembled the following:

```python
# models.py
from django.db import models
from django_fsm import FSMField
from django_fsm import transition


class Import(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        ERROR = "ERROR", "Error"
        COMPLETE = "COMPLETE", "Complete"

    status = FSMField(choices=Status.choices, default=Status.UPLOADED, protected=True)

    @transition(field=status, source=Status.UPLOADED, target=Status.PROCESSING)
    def process(self):
        try:
            # do some processing
            ...
        except Exception as e:
            self.handle_error(e)

    @transition(field=status, source=[Status.UPLOADED, Status.PROCESSING], target=Status.ERROR)
    def handle_error(self, error: Exception):
        # handle error by sending notifications, etc...
        ...

    @transition(field=status, source=Status.PROCESSING, target=Status.COMPLETE)
    def mark_complete(self):
        # do any cleanup, send success notifications, etc...
        ...

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            self.process()
```