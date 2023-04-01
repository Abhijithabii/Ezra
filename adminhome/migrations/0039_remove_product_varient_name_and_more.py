# Generated by Django 4.1.5 on 2023-03-11 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0038_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='varient_name',
        ),
        migrations.RemoveField(
            model_name='productvarient',
            name='name',
        ),
        migrations.AddField(
            model_name='productvarient',
            name='varname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminhome.product'),
            preserve_default=False,
        ),
    ]
