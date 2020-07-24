import logging

import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required, user_passes_test
from graphene_file_upload.scalars import Upload

from main import models
from main.schema import utils
from main.schema.inputs import (ProductInput, ProductOfferInput,
                                ProfileUpdateInput, UserReportInput,
                                UploadImageInput)
from main.schema.types import (Product, ProductOffer, Profile, UserReport,
                               Wishlist)

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
        input = ProfileUpdateInput()

    profile = graphene.Field(Profile)

    @login_required
    def mutate(root, info, username, input=None):
        errors = []

        if input is None:
            errors.append("Must provide an input to perform mutation. ")
            return UpdateProfile(errors=errors, profile=None)
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
        product_id = graphene.Int(required=True)
        input = ProductOfferInput()

    offer = graphene.Field(ProductOffer)

    @login_required
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.BUYER)
    def mutate(root, info, product_id, input=None):
        errors = []
        try:
            product = models.Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            errors.append(f"Product to offer on, not found")
            return CreateOffer(errors=errors, offer=None)

        profile = info.context.user.profile
        if(product.seller == profile):
            errors.append(f"User cannot offer on their own product")
            return CreateOffer(errors=errors, offer=None)

        try:
            previous_offer = product.offers.get(offerer=profile)
        except ObjectDoesNotExist:
            previous_offer = None
        
        if (previous_offer):
            errors.append(f"You cannot create multiple offers")
            return CreateOffer(errors=errors, offer=None)

        if (not product.is_negotiable):
            message = input['message'] 
            offer = utils.create_offer(profile, product, amount = product.expected_price, message = message)
            viewlog.debug(f"New Offer: {offer.to_dict()}")

            return CreateOffer(errors=errors, offer=offer)
        
        try:
            assert input['amount'] != None
        except:
            errors.append(f"Missing argument 'amount'")
            return CreateOffer(errors=errors, offer=None)

        offer = utils.create_offer(profile, product, **input.__dict__)
        viewlog.debug(f"New Offer: {offer.to_dict()}")

        return CreateOffer(errors=errors, offer=offer)

class CreateUserReport(MutationPayload, graphene.Mutation):
    class Arguments:
        input = UserReportInput()

    user_report = graphene.Field(UserReport)

    @login_required
    def mutate(root, info, input=None):
        errors = []

        reported_by = info.context.user.profile
        user_report = utils.create_user_report(reported_by, **input.__dict__)
        viewlog.debug(f"{user_report.reported_user} reported by {user_report.reported_by} for {user_report.category}")

        return CreateUserReport(errors=errors, user_report=user_report)

class UploadImage(MutationPayload, graphene.Mutation):
    class Arguments:
        input = UploadImageInput()
        file = Upload(required=False)

    product = graphene.Field(Product)

    @login_required
    @user_passes_test(lambda user: user.profile.permission_level >= models.Profile.SELLER)
    def mutate(root, info, input=None):
        errors = []
        id = input.get('product_id')
        # id = input.get('product_id')

        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product with primary key {id} does not exist.")
            return UploadImage(errors=errors, product=None)

        if product.seller != info.context.user.profile:
            errors.append("You are not allowed to perform this action.")
            return UploadImage(errors=errors, product=None)

        files = info.context.FILES

        product = utils.add_images_to_product(files, id)
        viewlog.debug(f"Product created with details : {product.to_dict()}")

        return UploadImage(errors=errors,product=product)

# class UpdateOffer(MutationPayload, graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = ProductOfferInput()

#     offer = graphene.Field(ProductOffer)

#     @login_required
#     def mutate(root, info, id, input=None):
#         errors = []

#         try:
#             offer = models.ProductOffer.objects.get(id=id)
#         except ObjectDoesNotExist:
#             errors.append(f"Offer not found")
#             return UpdateOffer(errors=errors, offer=None)
        
#         if (offer.offerer == info.context.user.profile):
#             offer = utils.update_offer(offer, **input.__dict__)
#             return UpdateOffer(errors=errors, offer=offer)
#         else:
#             errors.append(f"Only the user can change his offer.")
#             return UpdateOffer(errors=errors, offer=None)


class Mutation:
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    update_profile = UpdateProfile.Field()
    update_wishlist = UpdateWishlist.Field()
    create_offer = CreateOffer.Field()
    create_user_report = CreateUserReport.Field()
    upload_image = UploadImage.Field()
    # update_offer = UpdateOffer.Field()
