# Generated by Django 3.1.5 on 2021-01-16 18:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_auto_20210114_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='paymentDetail',
        ),
        migrations.RemoveField(
            model_name='userorder',
            name='paymentDetail',
        ),
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 16, 18, 26, 43, 449975, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='PaymentDetail',
        ),
        migrations.DeleteModel(
            name='PaymentItem',
        ),
        migrations.DeleteModel(
            name='PaymentTypes',
        ),
    ]
