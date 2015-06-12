# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0006_auto_20150611_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rater',
            name='age',
            field=models.IntegerField(choices=[(1, 'Under 18'), (18, '18-24'), (25, '25-34'), (35, '35-44'), (45, '45-49'), (50, '50-55'), (56, '56+')]),
        ),
        migrations.AlterField(
            model_name='rater',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('rater', 'movie')]),
        ),
    ]
