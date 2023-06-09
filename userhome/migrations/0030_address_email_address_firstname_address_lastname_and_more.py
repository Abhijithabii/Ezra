# Generated by Django 4.1.7 on 2023-03-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0029_alter_address_city_alter_address_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='firstname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
    ]
