# Generated by Django 4.1.7 on 2023-02-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0018_product_imag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
