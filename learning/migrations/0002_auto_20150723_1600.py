# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='tags',
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.ForeignKey(related_name='courses', verbose_name='tag', default=0, to='learning.Tag'),
            preserve_default=False,
        ),
    ]
