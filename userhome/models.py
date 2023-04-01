from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.



STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','Karnataka'),
    ('AndraPradesh','AndraPradesh')
)
DIST_CHOICES = {
    ('Kannur','Kannur'),
    ('Kozhikkode','Kozhikkode'),
    ('Ernakulam','Ernakulam'),
    ('Thiruvananthapuram','Thiruvananthapuram'),
    ('Banglore','Banglore'),
    ('Hubli','Hubli'),
    ('Hydrabad','Hydrabad'),
    ('Coimbator','Coimbator'),
    ('Madurai','Madurai'),
}

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10 ,null=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)
    district = models.CharField(choices=DIST_CHOICES,max_length=20, null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=20, null=True)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username








class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=200)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True)
    city = models.CharField(choices=DIST_CHOICES,max_length=255)
    state = models.CharField(choices=STATE_CHOICES,max_length=255)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.username
        


class Banner(models.Model):
    image = models.ImageField(upload_to='banner')
    title = models.CharField(max_length=300,null=True)
    desc = models.CharField(max_length=200)



 
    