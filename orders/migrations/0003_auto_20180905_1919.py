# Generated by Django 2.0 on 2018-09-05 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20180903_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('shipped', 'Shipped'), ('paid', 'Paid')], default='created', max_length=120),
        ),
    ]
