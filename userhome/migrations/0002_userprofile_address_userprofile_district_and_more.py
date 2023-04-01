# Generated by Django 4.1.7 on 2023-02-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picode',
            field=models.IntegerField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
