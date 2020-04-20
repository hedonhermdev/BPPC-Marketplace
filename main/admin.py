from django.contrib import admin
from .models import Product, Profile, RateUsers, QuesAndAnswer, ProductBid, ProductImage

admin.site.register(Profile)
admin.site.register(RateUsers)
admin.site.register(Product)
admin.site.register(QuesAndAnswer)
admin.site.register(ProductBid)
admin.site.register(ProductImage)
