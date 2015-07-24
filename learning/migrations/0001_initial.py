# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import learning.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(verbose_name='réponse', max_length=50)),
                ('order', models.PositiveIntegerField(verbose_name='ordre')),
                ('valid', models.BooleanField(default=False, verbose_name='réponse vraie')),
            ],
            options={
                'verbose_name': 'réponse',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='nom', max_length=50)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('standard_duration', models.DurationField(default=datetime.timedelta(1), verbose_name='durée standard')),
            ],
            options={
                'verbose_name_plural': 'cours',
                'verbose_name': 'cours',
            },
        ),
        migrations.CreateModel(
            name='CourseAttribution',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateTimeField(verbose_name='date')),
                ('duration', models.DurationField(verbose_name='durée')),
            ],
            options={
                'verbose_name_plural': 'attributions de cours',
                'verbose_name': 'attribution de cours',
            },
        ),
        migrations.CreateModel(
            name='CourseIntervalAttribution',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('begin', models.DateTimeField(verbose_name='début')),
                ('end', models.DateTimeField(verbose_name='fin')),
                ('course_attribution', models.ForeignKey(verbose_name='cours planifié', related_name='intervals', to='learning.CourseAttribution')),
            ],
            options={
                'verbose_name_plural': 'intervalles d’attributions de cours',
                'verbose_name': 'intervalle d’attribution de cours',
            },
        ),
        migrations.CreateModel(
            name='DayAttribution',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('day', models.DateField(verbose_name='jour')),
            ],
            options={
                'verbose_name_plural': 'attributions de jours',
                'verbose_name': 'attribution de jour',
            },
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='nom', max_length=50)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('days_count', models.PositiveIntegerField(verbose_name='nombre de jours')),
            ],
            options={
                'verbose_name': 'formation',
            },
        ),
        migrations.CreateModel(
            name='LectureFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(upload_to='lectures')),
                ('type', models.CharField(verbose_name='type MIME de fichier', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('avatar', models.ImageField(upload_to='avatar')),
                ('type', models.CharField(choices=[('student', 'élève'), ('teacher', 'formateur'), ('admin', 'administrateur')], verbose_name='type', max_length=10)),
            ],
            options={
                'verbose_name': 'Membre',
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='nom', max_length=50)),
                ('points', models.PositiveIntegerField(verbose_name='nombre de points')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'objectif',
            },
        ),
        migrations.CreateModel(
            name='ObjectiveAttribution',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('day', models.DateField(verbose_name='jour')),
                ('objective', models.ForeignKey(verbose_name='objectif', related_name='attributed_courses', to='learning.Objective')),
            ],
            options={
                'verbose_name_plural': 'attributions d’objectifs',
                'verbose_name': 'attribution d’objectif',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='promotion', max_length=50)),
                ('image', models.ImageField(upload_to='promotion', verbose_name='avatar de la promotion')),
                ('formation_type', models.ForeignKey(verbose_name='type de formation', related_name='promotions', to='learning.Formation')),
                ('group', models.OneToOneField(verbose_name='groupe', related_name='promotion', to='auth.Group')),
            ],
            options={
                'verbose_name': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(verbose_name='intitulé', max_length=50)),
                ('order', models.PositiveIntegerField(verbose_name='ordre')),
                ('question_type', models.CharField(choices=[('mono', 'une seule réponse'), ('multi', 'plusieurs réponses')], verbose_name='type de question', max_length=10)),
            ],
            options={
                'verbose_name': 'question',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='nom', max_length=50)),
                ('color', models.CharField(max_length=7, verbose_name='couleur', validators=[learning.validators.colorValidator])),
            ],
            options={
                'verbose_name': 'tag',
            },
        ),
        migrations.CreateModel(
            name='LectureCourse',
            fields=[
                ('course_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='learning.Course')),
                ('content', models.TextField(verbose_name='contenu')),
            ],
            options={
                'verbose_name': 'cours théorique',
            },
            bases=('learning.course',),
        ),
        migrations.CreateModel(
            name='PracticeCourse',
            fields=[
                ('course_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='learning.Course')),
                ('instructions', models.TextField(verbose_name='instructions')),
                ('repository', models.URLField(verbose_name='dépôt')),
            ],
            options={
                'verbose_name': 'cours pratique',
            },
            bases=('learning.course',),
        ),
        migrations.CreateModel(
            name='QuestionCourse',
            fields=[
                ('course_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='learning.Course')),
            ],
            options={
                'verbose_name': 'questionnaire',
            },
            bases=('learning.course',),
        ),
        migrations.AddField(
            model_name='objectiveattribution',
            name='promotion',
            field=models.ForeignKey(verbose_name='promotion', related_name='objectives', to='learning.Promotion'),
        ),
        migrations.AddField(
            model_name='member',
            name='tags',
            field=models.ManyToManyField(to='learning.Tag', verbose_name='tags', related_name='members'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(verbose_name='utilisateur', related_name='member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formation',
            name='objectives',
            field=models.ManyToManyField(to='learning.Objective', verbose_name='objectifs', related_name='formations'),
        ),
        migrations.AddField(
            model_name='formation',
            name='tags',
            field=models.ManyToManyField(to='learning.Tag', verbose_name='tags', related_name='formations'),
        ),
        migrations.AddField(
            model_name='dayattribution',
            name='assigned',
            field=models.ForeignKey(verbose_name='formateur', related_name='days', to='learning.Member'),
        ),
        migrations.AddField(
            model_name='dayattribution',
            name='promotion',
            field=models.ForeignKey(verbose_name='promotion', related_name='days', to='learning.Promotion'),
        ),
        migrations.AddField(
            model_name='dayattribution',
            name='tag',
            field=models.ForeignKey(verbose_name='tag', related_name='days', to='learning.Tag'),
        ),
        migrations.AddField(
            model_name='courseattribution',
            name='course',
            field=models.ForeignKey(verbose_name='cours', related_name='course_attributions', to='learning.Course'),
        ),
        migrations.AddField(
            model_name='courseattribution',
            name='promotion',
            field=models.ForeignKey(verbose_name='promotion', related_name='courses', to='learning.Promotion'),
        ),
        migrations.AddField(
            model_name='course',
            name='dependencies',
            field=models.ManyToManyField(to='learning.Objective', verbose_name='dépendances', related_name='dependant_courses'),
        ),
        migrations.AddField(
            model_name='course',
            name='objectives',
            field=models.ManyToManyField(to='learning.Objective', verbose_name='objectifs apportés', related_name='courses'),
        ),
        migrations.AddField(
            model_name='course',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, related_name='polymorphic_learning.course_set+', to='contenttypes.ContentType', editable=False),
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(to='learning.Tag', verbose_name='tags', related_name='courses'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='learning.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(verbose_name='questionnaire', related_name='questions', to='learning.QuestionCourse'),
        ),
        migrations.AlterUniqueTogether(
            name='objectiveattribution',
            unique_together=set([('promotion', 'objective')]),
        ),
        migrations.AddField(
            model_name='lecturefile',
            name='course',
            field=models.ForeignKey(verbose_name='cours', related_name='files', to='learning.LectureCourse'),
        ),
        migrations.AlterUniqueTogether(
            name='courseattribution',
            unique_together=set([('promotion', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('course', 'order')]),
        ),
    ]
