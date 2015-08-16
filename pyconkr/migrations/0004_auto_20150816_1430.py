# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pyconkr', '0003_auto_20150523_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('merchant_uid', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255)),
                ('company', models.CharField(max_length=100, blank=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('transaction_code', models.CharField(max_length=36)),
                ('payment_method', models.CharField(default=b'card', max_length=20, choices=[(b'card', '\uc2e0\uc6a9\uce74\ub4dc')])),
                ('payment_status', models.CharField(max_length=10)),
                ('payment_message', models.CharField(max_length=255, null=True)),
                ('vbank_num', models.CharField(max_length=255, null=True, blank=True)),
                ('vbank_name', models.CharField(max_length=20, null=True, blank=True)),
                ('vbank_date', models.CharField(max_length=50, null=True, blank=True)),
                ('vbank_holder', models.CharField(max_length=20, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='announcement',
            name='title_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='jobfair',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jobfair',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='program',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='program',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='programcategory',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='programtime',
            name='name_ja',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='room',
            name='name_ja',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='speaker',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='speaker',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='sponsorlevel',
            name='desc_ja',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sponsorlevel',
            name='name_ja',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='language',
            field=models.CharField(default=b'ko', max_length=2, choices=[(b'ko', b'Korean'), (b'en', b'English'), (b'ja', b'Japanese')]),
        ),
    ]
