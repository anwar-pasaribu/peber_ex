# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import peber_web.models


class Migration(migrations.Migration):

    dependencies = [
        ('peber_web', '0005_auto_20151031_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_corp',
            field=models.ForeignKey(related_name='news_sources', to='peber_web.News_Source'),
        ),
        migrations.AlterField(
            model_name='userdesc',
            name='profile_pict',
            field=models.ImageField(upload_to=peber_web.models.get_upload_file_name, blank=True),
        ),
        migrations.AlterField(
            model_name='userdesc',
            name='user',
            field=models.ForeignKey(related_name='userdescs', to=settings.AUTH_USER_MODEL),
        ),
    ]
