# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peber_web', '0004_auto_20151026_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdesc',
            old_name='user_info',
            new_name='user',
        ),
    ]
