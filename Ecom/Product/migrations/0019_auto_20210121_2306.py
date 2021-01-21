# Generated by Django 3.1.5 on 2021-01-21 23:06

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0018_auto_20210121_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cart',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 23, 6, 17, 541547, tzinfo=utc)),
        ),
    ]
