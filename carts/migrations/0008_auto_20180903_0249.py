# Generated by Django 2.0 on 2018-09-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
