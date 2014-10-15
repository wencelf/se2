# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0004_startup_minprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='askingPrice',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='last_price',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='minPrice',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]
