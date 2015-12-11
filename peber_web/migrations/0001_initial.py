# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peber_web.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_url', models.TextField()),
                ('news_title', models.TextField()),
                ('news_content', models.TextField()),
                ('news_summary', models.TextField()),
                ('news_pub_date', models.DateTimeField()),
                ('news_image_hero', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='News_Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_publisher', models.CharField(max_length=100)),
                ('source_category', models.CharField(max_length=100)),
                ('source_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=150)),
                ('profile_pict', models.FileField(upload_to=peber_web.models.get_upload_file_name)),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='news_corp',
            field=models.ForeignKey(to='peber_web.News_Source'),
        ),
    ]
