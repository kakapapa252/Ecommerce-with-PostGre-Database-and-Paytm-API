# Generated by Django 3.1.5 on 2021-01-22 16:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0020_auto_20210122_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='isDeleted',
        ),
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 22, 16, 18, 53, 842770, tzinfo=utc)),
        ),
    ]
