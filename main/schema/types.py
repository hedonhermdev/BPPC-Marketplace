import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from main import models
from main.models import HOSTEL_CHOICES


class ProductBid(DjangoObjectType):
    class Meta:
        model = models.ProductBid
        fields = ['bidder', 'product', 'amount', 'message']

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
        fields = ['id', 'name', 'seller', 'base_price', 'bids', 'description', 'category', 'visible', 'sold'] 
        filter_fields = {
            'visible': ['exact'],
            'sold': ['exact'],
            'base_price': ['gt', 'lt']
        }

    images = graphene.List(graphene.String)
    bids = graphene.List(ProductBid)
    questions = graphene.List(ProductQnA)
    reports = graphene.List(ProductReport)
    
    @staticmethod
    def resolve_images(self):
        return [i.image.url for i in self.images()]
    
    @staticmethod
    def resolve_bids(self, info, **kwargs):
        return self.bids.all()

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
    profile_picture = graphene.String()
    hostel = graphene.String()
    products = graphene.List(Product)

    @staticmethod
    def resolve_username(self, info, **kwargs):
        return self.user.username

    @staticmethod
    def resolve_profile_picture(self, info, **kwargs):
        return self.profile_picture.image.url
    
    @staticmethod
    def resolve_hostel(self, info, **kwargs):
        return getattr(HOSTEL_CHOICES, self.hostel, '')
       
    @staticmethod
    def resolve_products(self, info, **kwargs):
        return self.products.all()

