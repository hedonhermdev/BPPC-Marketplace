import graphene

class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    base_price = graphene.Int()
    description = graphene.String()
    sold = graphene.Boolean()
    category_id = graphene.Int()

class ProfileInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    hostel = graphene.String()
    contact_no = graphene.Int()

class ProductOfferInput(graphene.InputObjectType):
    id = graphene.ID()
    amount = graphene.Int()
    message = graphene.String()
    
