# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shares', models.DecimalField(max_digits=4, decimal_places=0)),
                ('timeStamp', models.DateField(auto_now_add=True, null=True)),
                ('price', models.DecimalField(max_digits=4, decimal_places=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cash', models.PositiveIntegerField(default=10, null=True)),
                ('phone', models.IntegerField(null=True)),
                ('twitter', models.CharField(max_length=100, null=True)),
                ('imagen', models.ImageField(default=b'', max_length=500, null=True, upload_to=b'photos')),
                ('imgurl', models.URLField(default=b'', max_length=500, null=True)),
                ('testfield', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startupName', models.CharField(max_length=100)),
                ('askingPrice', models.PositiveIntegerField(null=True)),
                ('last_price', models.PositiveIntegerField(null=True)),
                ('ceo', models.ForeignKey(to='stockmarket.Investor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bank',
            name='buyer',
            field=models.ForeignKey(to='stockmarket.Investor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bank',
            name='seller',
            field=models.ForeignKey(to='stockmarket.Startup'),
            preserve_default=True,
        ),
    ]
