from django.contrib import admin
from main.models import (
    Profile,
    Product,
    ImageModel,
    ProductBid,
    ProductQnA,
    ProfileRating,
    ProductReport,
    Category,
    Wishlist
)

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ImageModel)
admin.site.register(ProductBid)
admin.site.register(ProductQnA)
admin.site.register(ProfileRating)
admin.site.register(ProductReport)
admin.site.register(Category)
admin.site.register(Wishlist)
