# Generated by Django 2.0 on 2018-10-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20180919_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('billing', '-'), ('shipping', 'Shipping')], max_length=120),
        ),
    ]