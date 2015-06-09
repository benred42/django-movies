# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movieID',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='raterID',
            new_name='rater',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='movieID',
        ),
        migrations.RemoveField(
            model_name='rater',
            name='raterID',
        ),
        migrations.AlterField(
            model_name='rater',
            name='gender',
            field=models.CharField(max_length=1),
        ),
    ]
