import graphene
from graphql_jwt.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from main.schema.inputs import ProductInput, ProfileInput, ProductOfferInput
from main.schema.types import Product, Profile, Wishlist, ProductOffer
from main.schema import utils

from main import models

import logging

viewlog = logging.getLogger("viewlog")


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
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.SELLER)
    def mutate(root, info, input=None):
        errors = []

        seller = info.context.user.profile
        product = utils.create_product(seller, **input.__dict__)
        viewlog.debug(f"Product created with details : {product.to_dict()}")

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


class UpdateProfile(MutationPayload, graphene.Mutation):
    class Arguments:
        username = graphene.String(required = True)
        input = ProfileInput()

    profile = graphene.Field(Profile)

    @login_required
    def mutate(root, info, username, input=None):
        errors = []

        if input is None:
            errors.append("Must provide an input to perform mutation. ")
            return UpdateProfile(errors=erros, profile=None)
        try:
            profile = models.User.objects.get(username=username).profile
        except ObjectDoesNotExist:
            errors.append(f"Profile with username {username} does not exist")
            return UpdateProfie(errors=errors, profile=None)

        if profile.user != info.context.user:
            errors.append(f"Users are allowed to update only their respective profile.")
            return UpdateProfile(errors=errors, profile=None)

        profile = utils.update_profile(profile, **input.__dict__)
        viewlog.debug(f"Profile Updated: {profile.to_dict()}")

        return UpdateProfile(errors=errors, profile=profile)


class UpdateWishlist(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    wishlist = graphene.Field(Wishlist)

    @login_required
    def mutate(root, info, id, input=None):
        errors = []

        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product requested to add, not found ")
            return UpdateWishlist(errors=errors, wishlist=None)
        if(product.seller == info.context.user.profile):
            errors.append(f"User can't add his product to wishlist.")
            return UpdateWishlist(errors=errors, wishlist=None)
        wishlist = info.context.user.profile.wishlist
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)

        return UpdateWishlist(errors=errors, wishlist=wishlist)


class CreateOffer(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductOfferInput()

    offer = graphene.Field(ProductOffer)

    @login_required
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.BUYER)
    def mutate(root, info, id, input=None):
        errors = []
        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product to offer on, not found")
            return CreateOffer(errors=errors, offer=None)

        profile = info.context.user.profile
        if(product.seller == profile):
            errors.append(f"User cannot offer on their own product")
            return CreateOffer(errors=errors, offer=None)

        try:
            previous_offer = list(models.ProductOffer.objects.filter(offerer=profile, product=product))[-1]
        except:
            previous_offer = None

        if(previous_offer and previous_offer.amount >= input.amount):
            errors.append(f"You cannot offer less than or equal to your previous offer")
            return CreateOffer(errors=errors, offer=None)

        offer = utils.create_offer(profile, product, **input.__dict__)
        viewlog.debug(f"New Offer: {offer.to_dict()}")

        return CreateOffer(errors=errors, offer=offer)


class UpdateOffer(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductOfferInput()

    offer = graphene.Field(ProductOffer)

    @login_required
    def mutate(root, info, id, input=None):
        errors = []

        try:
            offer = models.ProductOffer.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Offer not found")
            return UpdateOffer(errors=errors, offer=None)
        
        if (offer.offerer == info.context.user.profile):
            offer = utils.update_offer(offer, **input.__dict__)
            return UpdateOffer(errors=errors, offer=offer)
        else:
            errors.append(f"Only the user can change his offer.")
            return UpdateOffer(errors=errors, offer=None)


class Mutation:
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    update_profile = UpdateProfile.Field()
    update_wishlist = UpdateWishlist.Field()
    create_offer = CreateOffer.Field()
    update_offer = UpdateOffer.Field()

