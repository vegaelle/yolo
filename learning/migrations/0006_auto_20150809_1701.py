# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0005_auto_20150809_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='dependencies',
            field=models.ManyToManyField(to='learning.Objective', blank=True, verbose_name='dépendances', related_name='dependant_courses', null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='objectives',
            field=models.ManyToManyField(to='learning.Objective', blank=True, verbose_name='objectifs apportés', related_name='courses', null=True),
        ),
    ]
