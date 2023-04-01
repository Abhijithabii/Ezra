# Generated by Django 4.1.7 on 2023-03-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userhome', '0050_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner')),
                ('desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Coimbator', 'Coimbator'), ('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Coimbator', 'Coimbator'), ('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
    ]
