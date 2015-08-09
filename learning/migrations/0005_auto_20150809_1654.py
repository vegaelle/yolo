# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0004_auto_20150724_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseintervalattribution',
            name='course_attribution',
        ),
        migrations.RemoveField(
            model_name='courseintervalattribution',
            name='day',
        ),
        migrations.RemoveField(
            model_name='courseattribution',
            name='date',
        ),
        migrations.RemoveField(
            model_name='courseattribution',
            name='duration',
        ),
        migrations.AddField(
            model_name='courseattribution',
            name='begin',
            field=models.DateTimeField(verbose_name='date et heure de début',
                                       default=datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseattribution',
            name='end',
            field=models.DateTimeField(verbose_name='date et heure de fin',
                                       default=datetime.now()),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CourseIntervalAttribution',
        ),
    ]
