import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from main import models
from main.models import HOSTEL_CHOICES

        
class ProductOffer(DjangoObjectType):
    class Meta:
        model = models.ProductOffer
        fields = ['offerer', 'product', 'amount', 'message']

class ProductQnA(DjangoObjectType):
    class Meta:
        model = models.ProductQnA
        fields = ['product', 'question', 'answer', 'asked_by', 'is_answered']

class ProductReport(DjangoObjectType):
    class Meta:
        model = models.ProductReport
        fields = ['product', 'message', 'reported_by']


class Product(DjangoObjectType):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'seller', 'base_price', 'offers', 'description', 'category', 'visible', 'sold'] 
        filter_fields = {
            'visible': ['exact'],
            'sold': ['exact'],
            'base_price': ['gt', 'lt']
        }

    images = graphene.List(graphene.String)
    offers = graphene.List(ProductOffer)
    questions = graphene.List(ProductQnA)
    reports = graphene.List(ProductReport)
    
    @staticmethod
    def resolve_images(self, info, **kwargs):
        return [i.image.url for i in self.images.all()]
    
    @staticmethod
    def resolve_offers(self, info, **kwargs):
        return self.offers.all()

    @staticmethod
    def resolve_questions(self, info, **kwargs):
        return self.questions.all()

    def resolve_reports(self, info, **kwargs):
        return self.reports.all()


class Category(DjangoObjectType):
    class Meta:
        model = models.Category
        fields = ['name']
    products = graphene.List(Product)
    
    def resolve_products(self):
        return self.products.all()
                

class Profile(DjangoObjectType):
    class Meta:
        model = models.Profile
        fields = ['id', 'name', 'room_no', 'contact_no', 'rating', 'email']
        
    username = graphene.String()
    avatar = graphene.String()
    hostel = graphene.String()
    products = graphene.List(Product)
    offers = graphene.List(ProductOffer)

    @staticmethod
    def resolve_username(self, info, **kwargs):
        return self.user.username

    @staticmethod
    def resolve_avatar(self, info, **kwargs):
        try:
            return self.avatar.first().url
        except:
            return ""
    
    @staticmethod
    def resolve_hostel(self, info, **kwargs):
        return getattr(HOSTEL_CHOICES, self.hostel, '')
       
    @staticmethod
    def resolve_products(self, info, **kwargs):
        return self.products.all()

    @staticmethod
    def resolve_offers(self, info, **kwargs):
        return self.offers.all()



class Wishlist(DjangoObjectType):
    class Meta:
        model = models.Wishlist
    
    profile = graphene.Field(Profile)
    products = graphene.List(Product)

    @staticmethod
    def resolve_products(self, info, **kwargs):
        return self.products.all()

    @staticmethod
    def resovle_profile(self, info, **kwargs):
        return self.profile


class ProductPaginated(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(Product)

