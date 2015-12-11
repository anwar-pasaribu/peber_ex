# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peber_web', '0007_auto_20151201_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdesc',
            name='read_news',
            field=models.ManyToManyField(to='peber_web.News'),
        ),
    ]
