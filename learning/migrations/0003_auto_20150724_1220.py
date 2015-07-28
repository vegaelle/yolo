# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20150723_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecturefile',
            options={'verbose_name': 'support de cours', 'verbose_name_plural': 'supports de cours'},
        ),
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatar', null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, verbose_name='tags', related_name='members', to='learning.Tag'),
        ),
    ]
