# Generated by Django 2.0 on 2018-09-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20180911_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('shipped', 'Shipped'), ('created', 'Created')], default='created', max_length=120),
        ),
    ]
