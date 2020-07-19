import graphene


class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    expected_price = graphene.Int()
    is_negotiable = graphene.Boolean()
    description = graphene.String()
    category_id = graphene.Int()

class ProfileUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    hostel = graphene.String()
    contact_no = graphene.String()

class ProductOfferInput(graphene.InputObjectType):
    id = graphene.ID()
    amount = graphene.Int()
    message = graphene.String()

class UserReportInput(graphene.InputObjectType):
    reported_user = graphene.String()
    category = graphene.Int()
