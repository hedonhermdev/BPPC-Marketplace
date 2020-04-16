# Documents for Elastic Search
from django_elasticsearch_dsl.documents import Document
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry
from main.models import Profile, Product


# Commented this for now because it does not let you create a user. 
# FIXME
#@registry.register_document
class ProfileDocument(Document):

    hostel = fields.TextField(attr="hostel_to_string")

    class Index:
        name = "users"

    class Django:
        model = Profile
        fields = [
            "name",
            "room_no",
        ]


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = "products"

    class Django:
        model = Product
        fields = [
            "name",
            "category",
        ]
