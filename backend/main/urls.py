from django.urls import path
from .views import content, auth, index
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from marketplace.schema import schema

urlpatterns = [
    path("", index.index, name="index"),
    path("api/graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("auth/authenticate/", auth.authenticate, name="auth-authenticate"),
]
