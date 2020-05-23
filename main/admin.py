from django.contrib import admin
from main.models import (
    Profile,
    Avatar,
    Product,
    ImageModel,
    ProductOffer,
    ProductQnA,
    ProfileRating,
    UserReport,
    Category,
    Wishlist
)

admin.site.register(Avatar)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(ImageModel)
admin.site.register(ProductOffer)
admin.site.register(ProductQnA)
admin.site.register(ProfileRating)
admin.site.register(UserReport)
admin.site.register(Category)
admin.site.register(Wishlist)
