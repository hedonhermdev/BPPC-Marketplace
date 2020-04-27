from main import models


def create_product(seller, **kwargs, ):
    """
        Given the attributes of a product and a Profile(seller) instance, create a new product and save it to the database. Utility for the CreateProduct mutation. 
    """

    p = models.Product()
    p.seller = seller
    p.name = kwargs.get('name')
    p.base_price = kwargs.get('base_price')
    p.description = kwargs.get('description')
    p.category_id = kwargs.get('category_id')
    p.save()

    return p


def update_product(product, **kwargs):
    """
        Given a product instance, and a set of updates, update the product instance and save it to the database. Utility for the UpdateProduct mutation.
    Updatable attributes of product are:
    1. Name
    2. Base Price
    3. Description
    4. Category
    """
    fields = ['name', 'base_price', 'description', 'category_id']
    print(kwargs)
    for field in fields:
        update = kwargs.get(field)
        if update is not None:
            setattr(product, field, update)
    
    product.save()

    return product

def create_profile(user, **kwargs):

    profile = models.Profile()
    profile.user = user
    profile.name = kwargs.get('name')
    profile.hostel = kwargs.get('hostel')
    profile.room_no = kwargs.get('room_no')
    profile.contact_no = kwargs.get('contact_no')
    profile.email = kwargs.get('email')

    profile.save()

    return profile

def update_profile(profile, **kwargs):
    
    fields = ['name', 'hostel', 'room_no', 'contact_no']

    for field in fields:
        update = kwargs.get(field)
        if update is not None:
            setattr(profile, field, update)

    profile.save()

    return profile

def create_bid(profile, product, **kwargs):

    bid = models.ProductBid()
    bid.bidder = profile
    bid.product = product
    bid.amount = kwargs.get('amount')
    bid.message = kwargs.get('message')

    bid.save()

    return bid

def update_bid(bid, **kwargs):

    fields = ['amount', 'message']

    for field in fields:
        update = kwargs.get(field)
        if update is not None:
            setattr(bid, field, update)

    bid.save()

    return bid

def profile_rating(rating_for, rated_by, rating):
    """
    Given the attributes of rating_for(Profile) and rated_by(Profile) instance, create a
    """
    rate_profile = models.ProfileRating()
    rate_profile.rating_for = rating_for
    rate_profile.rated_by = rated_by
    rate_profile.rating = rating
    rate_profile.save()

    return rate_profile
