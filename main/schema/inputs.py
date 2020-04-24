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
    room_no = graphene.Int()
    contact_no = graphene.Int()
    email = graphene.String()
