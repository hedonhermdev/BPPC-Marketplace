import graphene
from graphql_jwt.decorators import login_required

from main.schema.inputs import (
    ProductInput
)

from main import models


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput()

    ok = graphene.Boolean()
    product = graphene
    
    @login_required
    def mutate(root, info, input=None):
        ok = True
        product = models.Product()
        product.name = input.name
        product.base_price = input.base_price
        product.category = input.category
        product.seller = info.context.user.profile
        product.description = input.description

class Mutation:
    create_product = CreateProduct.Field()

