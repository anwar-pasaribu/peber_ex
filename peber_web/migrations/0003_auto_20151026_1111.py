# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peber_web', '0002_auto_20151026_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdesc',
            old_name='user',
            new_name='user_data',
        ),
    ]
