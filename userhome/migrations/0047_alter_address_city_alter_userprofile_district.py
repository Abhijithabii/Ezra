# Generated by Django 4.1.7 on 2023-03-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0046_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Banglore', 'Banglore'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai'), ('Ernakulam', 'Ernakulam'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Kozhikkode', 'Kozhikkode'), ('Hubli', 'Hubli'), ('Banglore', 'Banglore'), ('Hydrabad', 'Hydrabad'), ('Madurai', 'Madurai'), ('Ernakulam', 'Ernakulam'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=20, null=True),
        ),
    ]
