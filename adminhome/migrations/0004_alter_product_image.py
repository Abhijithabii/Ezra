# Generated by Django 4.1.7 on 2023-02-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='Product'),
        ),
    ]
