# Generated by Django 4.1.7 on 2023-02-23 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0019_alter_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveBigIntegerField(),
        ),
    ]
