# Generated by Django 5.0.6 on 2024-07-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_shippingaddress_product_ship'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
