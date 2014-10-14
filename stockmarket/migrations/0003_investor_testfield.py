# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0002_remove_investor_testfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='testfield',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
