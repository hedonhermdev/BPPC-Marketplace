from django.urls import path
from .views import content, auth

urlpatterns = [
<<<<<<< HEAD
    path("api/get_products/", content.get_products, name="get-products"),
    path("api/add_product/", content.add_product, name="add-product"),
    path(
        "api/get_product_detail/<int:id>", content.product_detail, name="product-detail"
    ),
    path("api/get_profile/<int:id>", content.get_profile, name="get-profile"),
    path("api/rate_user", content.rate_user, name="rate-user"),
    path("api/search_product", content.search_product, name="search-product"),
    path(
        "api/interested_buyers/<int:id>",
        content.interested_buyers,
        name="interested-buyers",
    ),
    path("auth/login/", auth.login, name="auth-login"),
    path("auth/register/", auth.register, name="auth-register"),
]
=======
    path('api/get_products/',content.get_products,name='get-products'),
    path('api/add_product/',content.add_product,name='add-product'),
    path('api/get_product_detail/<int:id>',content.product_detail,name='product-detail'),
    path('api/get_profile/<int:id>',content.get_profile,name='get-profile'),
    path('api/get_product_detail/sell_product/<int:id>',content.sell_product,name='sell-product'),
    path('api/get_user_products/<int:id>',content.user_products,name='user-products'),
>>>>>>> 5235e4b6758e5ff17ec01751154a3fa911b4785b

