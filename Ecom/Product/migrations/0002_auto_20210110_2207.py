# Generated by Django 3.1.5 on 2021-01-10 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='deliveryAddress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='User.addressdetail'),
        ),
        migrations.AddField(
            model_name='userorder',
            name='paymentDetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.paymentdetail'),
        ),
        migrations.AddField(
            model_name='userorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.product'),
        ),
        migrations.AddField(
            model_name='userorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Product.category'),
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='shippingAdresses',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.addressdetail'),
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='shippingType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Product.shippingtypes'),
        ),
        migrations.AddField(
            model_name='product',
            name='packageDetail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Product.packagedetails'),
        ),
        migrations.AddField(
            model_name='product',
            name='paymentDetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Product.paymentdetail'),
        ),
        migrations.AddField(
            model_name='product',
            name='shippingDetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Product.shippingdetails'),
        ),
        migrations.AddField(
            model_name='product',
            name='subCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnails',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.thumbnail'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='paymentItems',
            field=models.ManyToManyField(to='Product.PaymentItem'),
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.paymenttypes'),
        ),
        migrations.AddField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
        ),
    ]
