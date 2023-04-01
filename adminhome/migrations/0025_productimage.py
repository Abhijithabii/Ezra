# Generated by Django 4.1.7 on 2023-03-03 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0024_delete_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='media')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminhome.product')),
            ],
        ),
    ]
