from django.test import TestCase

from main.models import User, Profile, ProfileRating, Category, Product, ProductOffer
from main.auth_helpers import create_user_from_email

import random

class TestUserProfile(TestCase):
    def create_bitsian_user(self):
        email = "f20190120@pilani.bits-pilani.ac.in"
        user = create_user_from_email(email)
        return user
    
    def create_non_bitsian_user(self):
        email = "test_username@domain.com"
        user = create_user_from_email(email)
        return user
    
    def test_bitsian_user(self):
        user = self.create_bitsian_user()
        self.assertEqual(user.username, "f20190120")
        profile = user.profile
        self.assertEqual(profile.email, "f20190120@pilani.bits-pilani.ac.in")
        self.assertEqual(profile.permission_level, Profile.SELLER)
    
    def test_non_bitsian_user(self):
        user = self.create_non_bitsian_user()
        self.assertEqual(user.username, "test_username")
        profile = user.profile
        self.assertEqual(profile.email, "test_username@domain.com")
        self.assertEqual(profile.permission_level, Profile.BUYER)
    
    def test_profile_is_complete(self):
        user = self.create_bitsian_user()
        profile = user.profile
        self.assertEqual(profile.is_complete, False)
        profile.name = "John Doe"
        profile.hostel = "SR"
        profile.contact_no = "+911234567890"
        profile.save()
        self.assertEqual(profile.is_complete, True)

class TestProfileRating(TestCase):
    def create_test_user(self, email):
        return create_user_from_email(email)
    
    def test_user_can_rate_user(self):
        RATING = 4.0
        profile1 = self.create_test_user("userone@gmail.com").profile
        profile2 = self.create_test_user("usertwo@gmail.com").profile
        rating = ProfileRating(rating_for=profile1,
                               rated_by=profile2, rating=RATING)
        rating.save()
        # Test that user's profile rating is updated.
        self.assertEqual(profile1.rating, RATING)

class TestProduct(TestCase):
    
    def create_test_user(self, email):
        return create_user_from_email(email)
    
    def create_test_category(self, name):
        category = Category(id=1, name=name)
        category.save()
        return category
    
    def create_test_product(self, name='bbc'):
        product_name = name
        profile1 = self.create_test_user("userone@gmail.com").profile
        expectedPrice = 100
        description = "Some unknown english words"
        category = self.create_test_category(name='xyzCategory')
        product = Product(name=product_name, seller=profile1,
                          expected_price=expectedPrice, description=description,
                          category=category)
        product.save()
        return product
        
    def test_product_is_visible(self):
        product = self.create_test_product()
        self.assertEqual(product.visible, True)
        product.visible = False
        product.save()
        self.assertEqual(product.visible, False)
    
    def test_product_is_ticket(self):
        product = self.create_test_product()
        self.assertEqual(product.is_ticket, False)
        product.is_ticket = True
        product.save()
        self.assertEqual(product.is_ticket, True)
    
    def test_product_is_sold(self):
        product = self.create_test_product()
        self.assertEqual(product.sold, False)
        product.sold = True
        product.save()
        self.assertEqual(product.sold, True)
    
    def test_add_product_no_description(self):
        product = Product()
        is_sellable = True
        product.name = "XYZ"
        product.expected_price = 20
        product.category = self.create_test_category(name='xxyz')
        product.seller = self.create_test_user("userone@gmail.com").profile
        try:
            product.save()
        except:
            is_sellable=False
        self.assertEqual(is_sellable,False)

class TestProductOffer(TestCase):
    def create_test_user(self, email):
        user = create_user_from_email(email)
        return user

    def create_test_product(self, product_price = 500, is_negotiable = False):
        name = "TechRe"
        seller = self.create_test_user('f20190000@pilani.bits-pilani.ac.in').profile
        description = "Mint condition"
        category = Category(name = "Books")
        product = Product(
            name=name,
            seller=seller,
            expected_price=expected_price,
            description=description,
            category=category,
            is_negotiable=is_negotiable
            )
        product.save()
        return product
    
    def create_test_offer(self, product_price = 500, offer_amount = None, is_negotiable = False):
        offerer = self.create_test_user('f20190001@pilani.bits-pilani.ac.in').profile
        product = self.create_test_product(product_price=product_price, is_negotiable=is_negotiable)
        message = 'Looks good, interested'
        offer = ProductOffer(offerer=offerer, product=product, amount=offer_amount, message=message)
        offer.save()
        return offer

    def offer_on_negotiable_product(self):
        amount = 500
        offer = create_test_offer(offer_amount = amount, is_negotiable = True)
        self.assertEqual(offer.amount, amount)
    
    def offer_on_non_negotiable_product(self):
        product_price = 500
        offer_amount = 1000
        offer = create_test_offer(product_price=product_price, offer_amount=offer_amount)
        self.assertEqual(offer.amount, product_price)

    def null_offer_on_non_negotiable_product(self):
        product_price = 500
        offer_amount = None
        offer = create_test_offer(product_price=product_price, offer_amount=offer_amount)
        self.assertEqual(offer.amount, product_price)

