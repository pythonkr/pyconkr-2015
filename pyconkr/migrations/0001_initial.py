# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('announce_after', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmailToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('token', models.CharField(unique=True, max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Jobfair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('slide_url', models.CharField(max_length=255, null=True, blank=True)),
                ('pdf_url', models.CharField(max_length=255, null=True, blank=True)),
                ('video_url', models.CharField(max_length=255, null=True, blank=True)),
                ('language', models.CharField(default=b'ko', max_length=2, choices=[(b'ko', b'Korean'), (b'en', b'English'), (b'ja', b'Japanase')])),
                ('is_recordable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ProgramTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('email', models.EmailField(db_index=True, max_length=255, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'speaker', blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default=dict, help_text='help-text-for-speaker-info', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('image', models.ImageField(null=True, upload_to=b'sponsor', blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('desc', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(blank=True, to='pyconkr.SponsorLevel', null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='category',
            field=models.ForeignKey(blank=True, to='pyconkr.ProgramCategory', null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='date',
            field=models.ForeignKey(blank=True, to='pyconkr.ProgramDate', null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='rooms',
            field=models.ManyToManyField(to='pyconkr.Room', blank=True),
        ),
        migrations.AddField(
            model_name='program',
            name='speakers',
            field=models.ManyToManyField(to='pyconkr.Speaker', blank=True),
        ),
        migrations.AddField(
            model_name='program',
            name='times',
            field=models.ManyToManyField(to='pyconkr.ProgramTime', blank=True),
        ),
        migrations.AddField(
            model_name='jobfair',
            name='sponsor',
            field=models.ForeignKey(to='pyconkr.Sponsor', null=True),
        ),
    ]
