# Generated by Django 4.1.7 on 2023-03-10 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0026_rename_quantity_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVarient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varient_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='varient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminhome.productvarient'),
        ),
    ]
