from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.db import transaction
from graphene_django.views import GraphQLView
from rest_framework.views import APIView

from django.contrib.auth.models import User
from main.models import Profile, Product, ProfileRating

from ..schema.utils import create_product, update_product, create_profile, update_profile, create_bid, update_bid, profile_rating

import logging

log = logging.getLogger("main")


@api_view(
    ["GET",]
)
# @permission_classes([IsAuthenticated])
def get_products(request):
    paginator = PageNumberPagination()
    query_set = Product.objects.all()
    context = paginator.paginate_queryset(query_set, request)
    products = [p.to_dict() for p in context if p.visible == True]
    return Response(products, status=status.HTTP_200_OK)


@api_view(
    ["POST",]
)
# @permission_classes([IsAuthenticated])
@transaction.atomic
def add_product(request):
    try:
        product = create_product(request.user.profile,**request.data)
        return Response(product.to_dict(), status=status.HTTP_201_CREATED)
    except:
        return Response({"error":"Unable to add product."},status=status.HTTP_400_BAD_REQUEST)
    


@cache_page(60 * 10)
@api_view(
    ["GET",]
)
# @permission_classes([IsAuthenticated])
def product_detail(request, id):
    try:
        required_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response(required_product.to_dict(), status=status.HTTP_200_OK)


@cache_page(60 * 10)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_profile(request, id):
    try:
        required_user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(
            {"error": "No Such User Exist"}, status=status.HTTP_404_NOT_FOUND
        )

    required_profile = required_user.profile

    return Response(required_profile.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def rate_user(request, id):
    rating = request.data["rating"]
    rating_for = Profile.objects.get(pk=id)
    rating_record = profile_rating(rating_for, request.user.profile, rating)

    return Response(rating_record.to_dict(), status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@cache_page(60 * 5)
def search_product(request):
    data = request.data
    products = Product.objects.all()
    if data["category"] is not None:
        products = products.filter(category=data["category"])
    if data["description"] is not None:
        products = products.filter(description__contains=data["description"])
    return Response(products.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@cache_page(60 * 5)
def interested_buyers(request, id):
    interested = request.user.profile
    product = Product.objects.get(pk=id)
    if interested in product.interested_buyers.all():
        product.interested_buyers.remove(interested)
    else:
        product.interested_buyers.add(interested)
    return Response(product.to_dict(), status=status.HTTP_201_CREATED)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def sell_product(request, id):
    try:
        required_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(
            {"error": "No Such Product Exits."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.id != required_product.seller.id:
        return Response(
            {"error": "Only seller can sell a product"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    required_product.sold = True
    return Response(required_product.to_dict(), status=status.HTTP_200_OK)


@cache_page(60 * 10)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def user_products(request):
    try:
        required_profile = request.user.profile
    except User.DoesNotExist:
        return Response(
            {"error": "No Such User Exist"}, status=status.HTTP_404_NOT_FOUND
        )

    my_products = [p.to_dict() for p in required_profile.my_items.all()]
    return Response({"products": my_products}, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def my_profile(request):
    my_profile = request.user.profile
    return Response(my_profile.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    user.profile.name = data["name"]
    user.profile.hostel = data["hostel"]
    user.profile.room_no = data["room_no"]
    user.profile.contact_no = data["contact_no"]
    user.profile.email = data["email"]

    user.save()

    return Response(user.profile.to_dict(), status=status.HTTP_200_OK)
