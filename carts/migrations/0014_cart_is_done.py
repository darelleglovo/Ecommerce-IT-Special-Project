# Generated by Django 2.0 on 2018-10-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0013_auto_20180929_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
