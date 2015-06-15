# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0007_auto_20150612_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='rater',
            name='occupation',
            field=models.IntegerField(choices=[(0, 'Other or not specified'), (1, 'Academic/educator'), (2, 'Artist'), (3, 'Clerical/admin'), (4, 'College/grad student'), (5, 'Customer service'), (6, 'Doctor/health care'), (7, 'Executive/managerial'), (8, 'Farmer'), (9, 'Homemaker'), (10, 'K-12 student'), (11, 'Lawyer'), (12, 'Programmer'), (13, 'Retired'), (14, 'Sales/marketing'), (15, 'Scientist'), (16, 'Self-employed'), (17, 'Technician/engineer'), (18, 'Tradesman/craftsman'), (19, 'Unemployed'), (20, 'Writer')]),
        ),
    ]
