# Generated by Django 4.1.7 on 2023-03-18 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0047_remove_productvarient_varprice_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvarient',
            name='proname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='adminhome.product'),
        ),
    ]
