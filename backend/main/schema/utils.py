from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from main import models


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )

    
def create_product(seller, files, **kwargs, ):
    """
        Given the attributes of a product and images and a Profile(seller) instance, create a new product and save it with respective ImageModels' to the database. Utility for the CreateProduct mutation. 
    """

    p = models.Product()
    p.seller = seller
    p.name = kwargs.get('name')
    p.expected_price = kwargs.get('expected_price')
    p.is_negotiable = kwargs.get('is_negotiable')
    p.description = kwargs.get('description')
    p.category_id = kwargs.get('category_id')

    p.save()

    return p


def update_product(product, **kwargs):
    """
        Given a product instance, and a set of updates, update the product instance and save it to the database. Utility for the UpdateProduct mutation.
    Updatable attributes of product are:
    1. Name
    2. Expected Price
    3. Description
    4. Category
    """
    fields = ['name', 'expected_price', 'description', 'category_id']
    print(kwargs)
    for field in fields:
        update = kwargs.get(field)
        if update is not None:
            setattr(product, field, update)
    
    product.save()

    return product

def update_profile(profile, **kwargs):
    
    fields = ['name', 'hostel', 'contact_no']

    for field in fields:
        update = kwargs.get(field)
        if update is not None:
            setattr(profile, field, update)

    profile.save()

    return profile

def create_offer(profile, product, **kwargs):

    offer = models.ProductOffer()
    offer.offerer = profile
    offer.product = product
    offer.amount = kwargs.get('amount')
    offer.message = kwargs.get('message')

    offer.save()

    return offer

def profile_rating(rating_for, rated_by, rating):
    """
    Given the attributes of rating_for(Profile) and rated_by(Profile) instance, create a new profile_rating and save it to the database. Utility for ProfileRating Mutation.
    """
    rate_profile = models.ProfileRating()
    rate_profile.rating_for = rating_for
    rate_profile.rated_by = rated_by
    rate_profile.rating = rating
    rate_profile.save()

    return rate_profile

def create_user_report(reported_by, **kwargs):
    """
        Given the attributes of a Profile(reported_user) and a Profile(reported_user) instance, create a new UserReport and save it to the database. Utility for the CreateUserReport mutation. 
    """
    reported_user = models.User.objects.get(username=kwargs.get('reported_user'))
    report = models.UserReport()
    report.reported_by = reported_by
    report.reported_user = reported_user.profile
    report.category = kwargs.get('category')

    report.save()

    return report

def add_images_to_product(files, id):
    """
        Given the attributes of a Product and its related images, create new ImageModels' and add them to respective images attribute of the respective Product
    """
    product = models.Product.objects.get(id=id)
    if len(files.keys()) != 0:
        for i in files.keys():
            print(files.keys())
            imag = models.ImageModel()
            imag.image = files[i]
            imag.save()
            product.images.add(imag)
    product.save()
    return product
# def update_offer(offer, **kwargs):

#     fields = ['amount', 'message']

#     for field in fields:
#         update = kwargs.get(field)
#         if update is not None:
#             setattr(offer, field, update)

#     offer.save()

#     return offer
