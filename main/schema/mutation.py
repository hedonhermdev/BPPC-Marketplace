import graphene
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from main.schema.inputs import (
    ProductInput
)

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

    @login_required
    def mutate(root, info, input=None):
        errors = []

        seller = info.context.user.profile
        product = utils.create_product(seller, **input.__dict__)

        return CreateProduct(errors=errors)


class UpdateProduct(MutationPayload, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductInput()
    
    @login_required
    def mutate(root, info, id, input=None):
        errors = []

        try:
            product = models.Product.objects.get(id=id)
        except ObjectDoesNotExist:
            errors.append(f"Product with primary key {id} does not exist.")
            return UpdateProduct(errors=errors)

        if product.seller != info.context.user.profile:
            errors.append("You are not allowed to perform this action.")
            return UpdateProduct(errors=errors)
        
        product = utils.update_product(product, **input.__dict__)

        return UpdateProduct(errors=errors)


class Mutation:
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()

