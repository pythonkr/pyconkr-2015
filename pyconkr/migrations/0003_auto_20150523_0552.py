# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyconkr', '0002_auto_20150506_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programcategory',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
        ),
    ]
