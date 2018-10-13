# Generated by Django 2.0 on 2018-10-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20181009_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=30)),
                ('fb_link', models.CharField(max_length=50)),
                ('fb_messenger_link', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=30)),
                ('open_hours', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'About us',
                'verbose_name_plural': 'About us',
            },
        ),
        migrations.AlterModelOptions(
            name='aboutus',
            options={'verbose_name': 'About us', 'verbose_name_plural': 'About us'},
        ),
    ]