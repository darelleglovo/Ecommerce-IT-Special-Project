# Generated by Django 2.0 on 2018-09-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('paid', 'Paid'), ('created', 'Created')], default='created', max_length=120),
        ),
    ]
