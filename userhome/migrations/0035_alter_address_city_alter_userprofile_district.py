# Generated by Django 4.1.7 on 2023-03-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0034_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Hubli', 'Hubli'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hubli', 'Hubli'), ('Kannur', 'Kannur'), ('Coimbator', 'Coimbator'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Kozhikkode', 'Kozhikkode'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=20, null=True),
        ),
    ]
