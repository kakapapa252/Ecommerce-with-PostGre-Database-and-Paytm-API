# Generated by Django 3.1.5 on 2021-01-24 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0035_auto_20210124_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 16, 1, 53, 13499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='productDetails',
            field=models.JSONField(),
        ),
    ]