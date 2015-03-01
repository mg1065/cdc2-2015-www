# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdc', '0005_auto_20150212_0140'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginSession',
        ),
    ]
