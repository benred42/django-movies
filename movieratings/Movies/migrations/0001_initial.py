# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('movieID', models.IntegerField()),
                ('title', models.CharField(max_length=300)),
                ('genre', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('raterID', models.IntegerField()),
                ('gender', models.CharField(max_length=300)),
                ('age', models.IntegerField()),
                ('occupation', models.IntegerField()),
                ('zipcode', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('rating', models.IntegerField()),
                ('timestamp', models.IntegerField()),
                ('movieID', models.ForeignKey(to='Movies.Movie')),
                ('raterID', models.ForeignKey(to='Movies.Rater')),
            ],
        ),
    ]
