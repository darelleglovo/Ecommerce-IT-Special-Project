# Generated by Django 2.0 on 2018-08-09 07:14

from django.db import migrations
import django.db.models.deletion
import image_cropping.fields
import products.models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20180809_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=image_cropping.fields.ImageCropField(blank=True, null=True, upload_to=products.models.upload_image_path),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='category', chained_model_field='category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Subcategory'),
        ),
    ]
