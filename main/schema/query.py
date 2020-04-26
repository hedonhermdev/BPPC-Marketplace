import graphene
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main.schema.types import (
    Category,
    Profile,
    Product,
    ProductBid
)

class Query:
    all_categories = graphene.List(Category)
    all_products = graphene.List(Product)
    all_profiles = graphene.List(Profile)
    category = graphene.List(Category)
    product = graphene.Field(Product, id=graphene.Int())
    profile = graphene.Field(Profile, id=graphene.Int())
    productBid = graphene.List(ProductBid, id=graphene.Int())
    my_wishlist = graphene.List(Product)

    def resolve_all_categories(self, info, **kwargs):
        return models.Category.objects.all()

    def resolve_all_products(self, info, **kwargs):
        return models.Product.objects.all()

    def resolve_all_profiles(self, info, **kwargs):
        return models.Profile.objects.all()

    def resolve_category(self, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return models.Category.objects.get(name=name)
        return None

    def resolve_product(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            try:
                return models.Product.objects.get(id=id)
            except ObjectDoesNotExist:
                return None
        return None

    def resolve_profile(self, info, **kwargs):
        username = kwargs.get('username')
        id = kwargs.get('id')
        email = kwargs.get('email')
        if username is not None:
            try:
                user = models.User.objects.get(username=username)
            except ObjectDoesNotExist:
                return None
            return user.profile

        if id is not None:
            try:
                return models.Profile.objects.get(id=id)
            except ObjectDoesNotExist:
                return None
        if email is not None:
            try:
                return models.Profile.objects.get(email=email)
            except ObjectDoesNotExist:
                return None
        return None

    def resolve_my_wishlist(self, info, **kwargs):
        profile = info.context.user.profile

        if profile is not None:
            return profile.wishlist.products.all()

        return None
        
    def resolve_productBid(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                product = models.Product.objects.get(id=id)
            except ObjectDoesNotExist:
                return None
            return product.bids.all()

        return None
