from main import models


def create_product(seller, **kwargs):
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
