# Generated by Django 4.1.7 on 2023-02-22 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0009_rename_name_productimage_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminhome.productimage'),
        ),
    ]
