# Generated by Django 3.1.5 on 2021-01-31 14:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0036_auto_20210124_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='searchKeywords',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 31, 14, 50, 35, 897818, tzinfo=utc)),
        ),
    ]