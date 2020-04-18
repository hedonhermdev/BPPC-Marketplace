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
from main.models import Profile, Product

import logging

log = logging.getLogger("main")

class PrivateGraphQLView(APIView, GraphQLView):
    permission_classes = [IsAuthenticated]
    pass

@api_view(
    ["GET",]
)
@permission_classes([IsAuthenticated])
def get_products(request):
    paginator = PageNumberPagination()
    query_set = Product.objects.all()
    context = paginator.paginate_queryset(query_set, request)
    products = [p.to_dict() for p in context]
    return Response(products, status=status.HTTP_200_OK)


@api_view(
    ["POST",]
)
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_product(request):
    data = request.data
    product = Product()
    if data["price"] is None:
        return Response(
            {"error": "Product should have a Price."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        validated_price = data["price"]

    product.seller = request.user
    product.price = validated_price
    product.interested_buyers = data["interested_buyers"]
    product.sold = data["sold"]
    product.is_ticket = data["is_ticket"]
    product.save()

    return Response(product.to_dict(), status=status.HTTP_201_CREATED)


@cache_page(60 * 10)
@api_view(
    ["GET",]
)
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def rate_user(request):
    data = request.data
    if data["rating"] is None:
        return Response(
            {"error": "seller is not rated."}, status=status.HTTP_400_BAD_REQUEST
        )

    RateUsers(
        rating_for=data["seller"], rated_by=request.user, rating=data["rating"]
    ).save()
    Profile.objects.filter(user=data["seller"]).save()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
@cache_page(60 * 5)
def interested_buyers(request, id):
    interested = request.data["interested_buyer"]
    product = Product.objects.get(pk=id)
    if interested_buyer in product.interested_buyers.all():
        product.interested_buyers.remove(interested)
    else:
        product.interested_buyers.add(interested)
    return Response(product.to_dict(), status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def user_products(request, id):
    try:
        required_user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(
            {"error": "No Such User Exist"}, status=status.HTTP_404_NOT_FOUND
        )

    my_products = [p.to_dict() for p in Product.objects.filter(seller_id=id)]
    return Response(my_products, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    my_profile = request.user.profile
    return Response(my_profile.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
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
