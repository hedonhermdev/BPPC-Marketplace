# Documents for Elastic Search
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from main.models import Profile, Product

@registry.register_document
class ProfileDocument(Document):

    hostel = fields.TextField(attr="hostel_to_string")
    
    class Index:
        name = 'users'

    class Django:
        model = Profile
        fields = [
            'name',
            'room_no',
        ]

@registry.register_document
class ProductDocument(Document):
    seller = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Index:
        name = 'products'

    class Django:
        model = Product
        fields = [
            'name',
            'category',
        ]

