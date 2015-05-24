# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pyconkr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='program',
            name='date',
            field=models.ForeignKey(blank=True, to='pyconkr.ProgramDate', null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='rooms',
            field=models.ManyToManyField(to='pyconkr.Room', blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='times',
            field=models.ManyToManyField(to='pyconkr.ProgramTime', blank=True),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='info',
            field=jsonfield.fields.JSONField(default=dict, help_text='help-text-for-speaker-info', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(blank=True, to='pyconkr.SponsorLevel', null=True),
        ),
    ]
