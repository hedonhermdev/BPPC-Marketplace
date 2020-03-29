from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from django.contrib.auth.models import User
from main.models import Profile,Product

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_products(request):
    products = [p.to_dict() for p in Product.objects.all()]
    return Response(products,status=status.HTTP_200_OK)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def add_product(request):
    data = request.data
    product = Product()
    if data['price'] is None:
        return Response({'error':'Product should have a Price.'},status=status.HTTP_400_BAD_REQUEST)
    else :
        validated_price = data['price']

    product.seller = User.objects.get(pk=data['seller'])
    product.price = validated_price
    product.interested_buyers = data['interested_buyers']
    product.sold = data['sold']
    product.is_ticket = data['is_ticket']
    product.save()

    return Response(product.to_dict(),status=status.HTTP_201_CREATED)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def product_detail(request,id):
    try:
        required_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)

    return Response(required_product.to_dict(),status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request,id):
    try:
        required_user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({'error':'No Such User Exist'},status=status.HTTP_404_NOT_FOUND)

    required_profile = required_user.profile

    return Response(required_profile.to_dict(),status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sell_product(request,id):
    try:
        required_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response({'error':'No Such Product Exits.'},status=status.HTTP_404_NOT_FOUND)
    
    if request.user.id != required_product.seller.id:
        return Response({'error':'Only seller can sell a product'},status=status.HTTP_400_BAD_REQUEST)
    
    required_product.sold = True
    return Response(required_product.to_dict(),status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_products(request,id):
    try:
        required_user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({'error':'No Such User Exist'},status=status.HTTP_404_NOT_FOUND)

    my_products = [p.to_dict() for p in Product.objects.filter(seller_id=id)]
    return Response(my_products,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes(IsAuthenticated])
def my_profile(request):
    my_profile = request.user.profile
    return Response(my_profile.to_dict(),status=status.HTTP_200_OK)
