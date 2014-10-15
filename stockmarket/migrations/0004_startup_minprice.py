# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0003_investor_testfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='minPrice',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
