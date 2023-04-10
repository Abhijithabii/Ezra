# Generated by Django 4.1.7 on 2023-04-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='wallet_amt',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=0, null=True),
        ),
    ]