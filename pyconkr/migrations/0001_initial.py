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
                ('title_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('title_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
                ('announce_after', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('token', models.CharField(unique=True, max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jobfair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
                ('slide_url', models.CharField(max_length=255, null=True, blank=True)),
                ('pdf_url', models.CharField(max_length=255, null=True, blank=True)),
                ('video_url', models.CharField(max_length=255, null=True, blank=True)),
                ('language', models.CharField(default=b'ko', max_length=2, choices=[(b'ko', b'Korean'), (b'en', b'English')])),
                ('is_recordable', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_ko', models.CharField(max_length=100, null=True)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_ko', models.CharField(max_length=100, null=True)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('email', models.EmailField(db_index=True, max_length=255, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'speaker', blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default=dict, help_text='<p>Add your personal pages in JSON format.</p>\n<pre>\n# Example\n{\n  "twitter": "https://twitter.com/ev",\n  "github": "https://github.com/defunkt"\n}\n</pre>\n<p>Supported pages are listed in <a href="http://lipis.github.io/bootstrap-social/" target="_blank">http://lipis.github.io/bootstrap-social/</a></p>', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('image', models.ImageField(null=True, upload_to=b'sponsor', blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('name_ko', models.CharField(max_length=100, null=True, db_index=True)),
                ('name_en', models.CharField(max_length=100, null=True, db_index=True)),
                ('slug', models.SlugField(max_length=100)),
                ('desc', models.TextField(null=True, blank=True)),
                ('desc_ko', models.TextField(null=True, blank=True)),
                ('desc_en', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(to='pyconkr.SponsorLevel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='category',
            field=models.ForeignKey(blank=True, to='pyconkr.ProgramCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='date',
            field=models.ForeignKey(to='pyconkr.ProgramDate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='rooms',
            field=models.ManyToManyField(to='pyconkr.Room', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='speakers',
            field=models.ManyToManyField(to='pyconkr.Speaker', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='times',
            field=models.ManyToManyField(to='pyconkr.ProgramTime'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobfair',
            name='sponsor',
            field=models.ForeignKey(to='pyconkr.Sponsor', null=True),
            preserve_default=True,
        ),
    ]
