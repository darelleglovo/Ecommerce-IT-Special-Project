# Generated by Django 2.0 on 2018-10-09 05:15

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0068_auto_20181009_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='category', chained_model_field='category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Subcategory'),
        ),
    ]
