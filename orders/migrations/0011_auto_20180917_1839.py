# Generated by Django 2.0 on 2018-09-17 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20180912_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('created', 'Created'), ('paid', 'Paid')], default='created', max_length=120),
        ),
    ]
