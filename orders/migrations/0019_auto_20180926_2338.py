# Generated by Django 2.0 on 2018-09-26 15:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20180924_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('credit_card', 'Credit Card'), ('bank_deposit', 'Bank Deposit')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('waiting_for_payment', 'Waiting for payment'), ('canceled', 'Canceled'), ('created', 'Created')], default='created', max_length=120),
        ),
    ]