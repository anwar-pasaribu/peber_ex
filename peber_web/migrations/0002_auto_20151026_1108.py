# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import peber_web.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peber_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDesc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.TextField(blank=True)),
                ('profile_pict', models.FileField(upload_to=peber_web.models.get_upload_file_name)),
                ('news_choices', models.ManyToManyField(to='peber_web.News_Source')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userdesc',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
