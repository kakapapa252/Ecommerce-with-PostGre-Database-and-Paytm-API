# Generated by Django 3.1.5 on 2021-01-12 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20210112_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonedetail',
            name='phType',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='User.phonetypes'),
        ),
    ]
