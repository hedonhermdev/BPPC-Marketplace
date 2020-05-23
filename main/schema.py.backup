import graphene
from graphql_jwt.decorators import login_required

from graphene_django.types import DjangoObjectType
from main.models import Profile, Product, ProductImage
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class ProductType(DjangoObjectType):

    class Meta:
        model = Product



class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage

class Query(object):
    product = graphene.Field(ProductType, id=graphene.Int(), name=graphene.String())
    all_products = graphene.List(ProductType)
    profile = graphene.Field(ProfileType, id=graphene.Int(), name=graphene.String())
    all_profiles = graphene.List(ProfileType)

    @login_required
    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    @login_required
    def resolve_all_profiles(self, info, **kwargs):
        return Profile.objects.all()
    
    @login_required
    def resolve_product(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Product.objects.get(pk=id)

        return None
    
    @login_required
    def resolve_profile(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Profile.objects.get(pk=id)

        return None


# Input Object Types
class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    base_price = graphene.Int(required=True)
    description = graphene.String()
    sold = graphene.Boolean()
    category = graphene.String()
    is_ticket = graphene.Boolean()
    created = graphene.DateTime()
    seller = ProductType()


class ProfileInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    hostel = graphene.String()
    room_no = graphene.Int()
    contact_no = graphene.Int()
    email = graphene.String()


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput()

    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    #@login_required
    def mutate(root, info, input=None):
        ok = True
        product_instance = Product()
        product_instance.base_price = input.base_price
        product_instance.name = input.name
        product_instance.description = input.description
        product_instance.category = input.category
        product_instance.save()
        return CreateProduct(ok=ok, product=product_instance)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductInput()

    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    @login_required
    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        product_instance = Product.Objects.get(pk=id)
        if product_instance:
            ok = True
            product_instance.name = input.name
            product_instance.description = input.description
            product_instance.category = input.category
            product_instance.base_price = input.base_price
            product_instance.sold = input.sold
            product_instance.save()
            return UpdateProduct(ok=ok, product=product_instance)
        return UpdateProduct(ok=ok, product=None)


class CreateProfile(graphene.Mutation):
    class Arguments:
        input = ProfileInput()

    ok = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    #@login_required
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        profile_instance = Profile(email=input.email)
        profile_instance.name = input.name
        profile_instance.hostel = input.hostel
        profile_instance.contact_no = input.contact_no
        profile_instance.room_no = input.room_no
        return CreateProfile(ok=ok, profile=profile_instance)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProfileInput()

    ok = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    @login_required
    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        profile_instance = Profile.Objects.get(pk=id)
        if profile_instance:
            profile_instance.name = input.name
            profile_instance.hostel = input.hostel
            profile_instance.contact_no = input.contact_no
            profile_instance.room_no = input.room_no
            profile_instance.email = input.email
            return UpdateProfile(ok=ok, profile=profile_instance)
        return UpdateProfile(ok=ok, product=None)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
