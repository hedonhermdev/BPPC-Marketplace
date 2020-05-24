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
    
class TestProductOffer(TestCase):
    def create_test_user(self, email):
        return create_user_from_email(email)
    
    def create_test_category(self, name):
        category = Category(name=name)
        category.save()
        return category

    def create_test_product(self):
        name = "TechRe Book" 
        seller = self.create_test_user('f20190000@pilani.bits-pilani.ac.in').profile
        product_price = 500
        description = "Mint condition"
        category = self.create_test_category(name = "Books")
        product = Product(
            name=name,
            seller=seller,
            expected_price=product_price,
            description=description,
            category=category,
            )
        product.save()
        return product
    
    def create_test_offer(self, amount = 100, email='f20190001@pilani.bits-pilani.ac.in', product=None):
        offerer = self.create_test_user(email=email).profile
        if product:
            product = product
        else:
            product = self.create_test_product()
        message = 'Looks good, interested'
        offer = ProductOffer(offerer=offerer, product=product, amount=amount, message=message)
        offer.save()
        return offer

    def test_offer(self):
        amount = 1000
        offer = self.create_test_offer(amount=amount)
        self.assertEqual(offer.amount, amount)
        self.assertEqual(offer.product.name, "TechRe Book")
        self.assertEqual(offer.offerer.email, "f20190001@pilani.bits-pilani.ac.in")
        self.assertEqual(offer.message, "Looks good, interested")

    def test_num_offers(self):
        # Create offer on a product and test product's no. of offers
        offer = self.create_test_offer(email="one@domain.com")
        self.assertEqual(offer.product.num_offers, 1)

        # Create another offer on the same product and test product's no. of offers
        offer = self.create_test_offer(email="two@domain.com", product=offer.product)
        self.assertEqual(offer.product.num_offers, 2)


