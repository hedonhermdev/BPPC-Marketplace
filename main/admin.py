from django.contrib import admin
from .models import Product, Profile, RateUsers

admin.site.register(Profile)
admin.site.register(RateUsers)
admin.site.register(Product)
