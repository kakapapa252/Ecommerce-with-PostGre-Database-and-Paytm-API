# Generated by Django 3.1.5 on 2021-01-24 14:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0026_auto_20210123_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 14, 12, 57, 548894, tzinfo=utc)),
        ),
    ]
