# Generated by Django 4.1.7 on 2023-02-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0011_alter_userprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
