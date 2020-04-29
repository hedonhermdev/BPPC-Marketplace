from django.urls import path
from .views import content, auth, index
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from marketplace.schema import schema

urlpatterns = [
    path("", index.index, name="index"),
    path("api/products/", content.get_products, name="get-products"),
    path("api/add_product/", content.add_product, name="add-product"),
    path(
        "api/product_detail/<int:id>", content.product_detail, name="product-detail"
    ),
    path("api/profile/<int:id>", content.get_profile, name="get-profile"),
    path("api/rate_user/<int:id>", content.rate_user, name="rate-user"),
    path(
        "api/interested_buyers/<int:id>",
        content.interested_buyers,
        name="interested-buyers",
    ),
    path("api/user_products/", content.user_products, name="user-products"),
    path("api/my_profile/", content.my_profile, name="my-profile"),
    path(
        "api/my_profile/update_profile/", content.update_profile, name="update-profile"
    ),
    path("api/graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path("auth/authenticate/", auth.authenticate, name="auth-authenticate"),


]
