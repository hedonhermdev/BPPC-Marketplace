from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from django.contrib.auth.models import User
from main.models import Profile, Product


@api_view(
    ["GET",]
)
@permission_classes([IsAuthenticated])
def get_products(request):
    products = [p.to_dict() for p in Product.objects.all()]
    return Response(products, status=status.HTTP_200_OK)


@api_view(
    ["POST",]
)
@permission_classes([IsAuthenticated])
def add_product(request):
    data = request.data
    product = Product()
    if data["price"] is None:
        return Response(
            "Product should have a Price.", status=status.HTTP_400_BAD_REQUEST
        )
    else:
        validated_price = data["price"]

    product.seller = User.objects.get(pk=data["seller"])
    product.price = validated_price
    product.interested_buyers = data["interested_buyers"]
    product.sold = data["sold"]
    product.is_ticket = data["is_ticket"]
    product.save()

    return Response(product.to_dict(), status=status.HTTP_201_CREATED)


@api_view(
    ["GET",]
)
@permission_classes([IsAuthenticated])
def product_detail(request, id):
    try:
        required_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

    return Response(required_product.to_dict(), status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request, id):
    try:
        required_user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response("No Such User Exist", status=status.HTTP_404_NOT_FOUND)

    required_profile = required_user.profile

    return Response(required_profile.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_user(request):
    data = request.data
    if data["rating"] is None:
        return Response("Rate Seller.", status=status.HTTP_400_BAD_REQUEST)

    RateUsers(
        rating_for=data["seller"], rated_by=request.user, rating=data["rating"]
    ).save()
    Profile.objects.filter(user=data["seller"]).save()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_product_by_category(request):
    data = request.data
    products = Product.objects.all()
    if data["category"] is not None:
        products = products.filter(category=data["category"])
    if data["description"] is not None:
        products = products.filter(description__contains=data["description"])
    return Response(products.to_dict(), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def interested_buyers(request, id):
    interested = request.data["interested_buyer"]
    product = Product.objects.get(pk=id)
    if interested_buyer in product.interested_buyers.all():
        product.interested_buyers.remove(interested)
    else:
        product.interested_buyers.add(interested)
    return Response(product.to_dict(), status=status.HTTP_201_CREATED)
