# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0008_auto_20150615_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(validators=[Movies.models.validate_rating_in_range]),
        ),
    ]
