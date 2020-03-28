from django.urls import path
from .views import content,auth

urlpatterns = [
    path('api/get_products/',content.get_products,name='get-products'),
    path('api/add_product/',content.add_product,name='add-product'),
    path('api/get_product_detail/<int:id>',content.product_detail,name='product-detail'),
    path('api/get_profile/<int:id>',content.get_profile,name='get-profile'),

    path('auth/login/',auth.login,name='auth-login'),
    path('auth/register/',auth.register,name='auth-register'),

]