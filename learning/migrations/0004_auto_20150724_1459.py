# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_auto_20150724_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseintervalattribution',
            name='day',
            field=models.ForeignKey(related_name='intervals', default=1, verbose_name='jour', to='learning.DayAttribution'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='tags',
            field=models.ManyToManyField(verbose_name='tags', related_name='members', blank=True, to='learning.Tag'),
        ),
    ]
