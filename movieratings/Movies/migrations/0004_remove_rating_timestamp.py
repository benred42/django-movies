# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0003_auto_20150610_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='timestamp',
        ),
    ]
