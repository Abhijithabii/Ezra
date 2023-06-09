# Generated by Django 4.1.7 on 2023-03-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0021_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Banglore', 'Banglore'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai')], max_length=20, null=True),
        ),
    ]
