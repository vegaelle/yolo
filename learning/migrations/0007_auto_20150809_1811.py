# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0006_auto_20150809_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='dependencies',
            field=models.ManyToManyField(blank=True, related_name='dependant_courses', to='learning.Objective', verbose_name='dépendances'),
        ),
        migrations.AlterField(
            model_name='course',
            name='objectives',
            field=models.ManyToManyField(blank=True, related_name='courses', to='learning.Objective', verbose_name='objectifs apportés'),
        ),
    ]
