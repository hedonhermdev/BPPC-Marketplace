from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

from marketplace.schema import schema

from .views import auth, content, index

urlpatterns = [
    path("", index.index, name="index"),
    path("api/graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
    path("auth/authenticate/", auth.authenticate, name="auth-authenticate"),
]
