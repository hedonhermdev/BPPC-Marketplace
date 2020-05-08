import graphene
from graphql_jwt.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from main.schema.inputs import ProductInput, ProfileInput, ProductBidInput
from main.schema.types import Product, Profile, Wishlist, ProductBid
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
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.SELLER)
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


class CreateBid(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductBidInput()

    bid = graphene.Field(ProductBid)

    @login_required
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.BUYER)
    def mutate(root, info, id, input=None):
        errors = []

        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product to bid on, not found")
            return CreateBid(errors=errors, bid=None)

        profile = info.context.user.profile
        if(product.seller == profile):
            errors.append(f"User can't bid on their on product")
            return CreateBid(errors=errors, bid=None)
        bid = utils.create_bid(profile, product, **input.__dict__)

        return CreateBid(errors=errors, bid=bid)


class UpdateBid(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductBidInput()

    bid = graphene.Field(ProductBid)

    @login_required
    def mutate(root, info, id, input=None):
        errors = []

        try:
            bid = models.ProductBid.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Bid not found")
            return UpdateBid(errors=errors, bid=None)
        
        if (bid.bidder == info.context.user.profile):
            bid = utils.update_bid(bid, **input.__dict__)
            return UpdateBid(errors=errors, bid=bid)
        else:
            errors.append(f"Only the user can change his bid")
            return UpdateBid(errors=errors, bid=None)


class Mutation:
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
    update_wishlist = UpdateWishlist.Field()
    create_bid = CreateBid.Field()
    update_bid = UpdateBid.Field()

