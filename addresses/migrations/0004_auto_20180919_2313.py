# Generated by Django 2.0 on 2018-09-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20180919_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('luzon', 'Luzon'), ('visayas', 'Visayas'), ('mindanao', 'Mindanao')], max_length=120),
        ),
    ]
