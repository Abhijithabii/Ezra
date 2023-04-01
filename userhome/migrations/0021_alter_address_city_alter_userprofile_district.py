# Generated by Django 4.1.7 on 2023-03-03 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0020_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad'), ('Banglore', 'Banglore')], max_length=20, null=True),
        ),
    ]
