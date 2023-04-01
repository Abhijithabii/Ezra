from django.contrib import admin
from .models import UserProfile, Address, Banner
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Banner)