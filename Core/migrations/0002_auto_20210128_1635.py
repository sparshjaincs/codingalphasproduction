# Generated by Django 3.1.5 on 2021-01-28 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 28, 16, 35, 23, 961072)),
        ),
        migrations.AlterField(
            model_name='anwsers',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 28, 16, 35, 23, 950956)),
        ),
        migrations.AlterField(
            model_name='aptitude',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 28, 16, 35, 23, 961072)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 28, 16, 35, 23, 950956)),
        ),
        migrations.AlterField(
            model_name='list',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 28, 16, 35, 23, 961072)),
        ),
    ]
