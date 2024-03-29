# Generated by Django 3.1.5 on 2021-01-10 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('categoryType', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PackageDetails',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('fragile', models.BooleanField(default=False)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('depth', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentItem',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('maxLength', models.IntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTypes',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('types', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('searchCriteria', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('incTax', models.BooleanField(default=False)),
                ('availableQt', models.PositiveIntegerField(default=0)),
                ('refundable', models.BooleanField(default=False)),
                ('refund_period', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField()),
                ('inProcessQt', models.IntegerField(default=0)),
                ('soldQt', models.IntegerField(default=0)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDetails',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('shippingPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingTypes',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('shippingType', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('subCategoryType', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('thumbnailDetail', models.CharField(blank=True, max_length=200, null=True)),
                ('isFirst', models.BooleanField(default=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shippingPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('paymentRecieved', models.BooleanField(default=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
