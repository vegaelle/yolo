# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_auto_20150809_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'cours', 'permissions': (('view_course', 'Can view a course'),), 'verbose_name_plural': 'cours'},
        ),
    ]
