import graphene
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from main.schema.inputs import ProductInput, ProfileInput
from main.schema.types import Product, Profile
from main.schema import utils

from main import models

class MutationPayload(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)
    query = graphene.Field('marketplace.schema.Query', required=True)

    def resolve_ok(self, info):
        return len(self.errors or []) == 0

    def resolve_errors(self, info):
        return self.errors or []

    def resolve_query(self, info):
        return {}

class CreateProduct(MutationPayload, graphene.Mutation):
    class Arguments:
        input = ProductInput()

    product = graphene.Field(Product)

    @login_required
    def mutate(root, info, input=None):
        errors = []

        seller = info.context.user.profile
        product = utils.create_product(seller, **input.__dict__)

        return CreateProduct(errors=errors,product=product)


class UpdateProduct(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductInput()
    
    product = graphene.Field(Product)

    @login_required
    def mutate(root, info, id, input=None):
        errors = []

        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product with primary key {id} does not exist.")
            return UpdateProduct(errors=errors, product=None)

        if product.seller != info.context.user.profile:
            errors.append("You are not allowed to perform this action.")
            return UpdateProduct(errors=errors, product=None)
        
        product = utils.update_product(product, **input.__dict__)

        return UpdateProduct(errors=errors, product=product)


class CreateProfile(MutationPayload, graphene.Mutation):
    class Arguments:
        input = ProfileInput()

    profile = graphene.Field(Profile)

    @login_required
    def mutate(root, info, input=None):
        errors = []

        user = info.context.user
        profile = utils.create_profile(user, **input.__dict__)

        return CreateProfile(errors=errors, profile = profile)


class UpdateProfile(MutationPayload, graphene.Mutation):
    class Arguments:
        username = graphene.String(required = True)
        input = ProfileInput()

    profile = graphene.Field(Profile)

    @login_required
    def mutate(root, info, username, input=None):
        errors = []

        try:
            profile = models.User.objects.get(username=username).profile
        except ObjectDoesNotExist:
            errors.append(f"Profile with username {username} does not exist")
            return UpdateProfie(errors=errors, profile=None)

        if profile.user != info.context.user:
            errors.append(f"Users are allowed to update only their respective profile.")
            return UpdateProfile(errors=errors, profile=None)

        profile = utils.upadate_profile(profile, **input.__dict__)

        return UpdateProfile(errors=errors, profile=profile)

class Mutation:
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()

