# Generated by Django 4.1.7 on 2023-03-11 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0041_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad')], max_length=20, null=True),
        ),
    ]
