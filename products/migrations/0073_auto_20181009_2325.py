# Generated by Django 2.0 on 2018-10-09 15:25

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0072_auto_20181009_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default='Colorless', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='odor',
            field=models.CharField(default='Not much usually', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default='1"x3"', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(default='6 ounces', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='category', chained_model_field='category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Subcategory'),
        ),
    ]
