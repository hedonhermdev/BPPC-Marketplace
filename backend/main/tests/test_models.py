from django.test import TestCase

from main.models import User, Profile, ProfileRating, Category, Product
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
        
        rating = ProfileRating(rating_for=profile1, rated_by=profile2, rating=RATING)
        rating.save()
        # Test that user's profile rating is updated.
        self.assertEqual(profile1.rating, RATING)

class TestProduct(TestCase):
    def create_test_user(self,email):
        return create_user_from_email(email)

    def create_test_category(self,name):
        category=Category(name=name)
        return category
    
    def create_test_product(self,name='bbc'):
        product_name=self.name
        profile1 = self.create_test_user("userone@gmail.com").profile
        basePrice = 100
        description = "Some unknown english words"
        category = create_test_category(name='xyzCategory')
        product = Product(name=product_name,seller=profile1,
                        base_price=basePrice,description=description,
                        category=category)
        product.save()
        return product
    
    def product_is_complete(self):
        product = Product()
        self.assertEqual(product.is_complete, False)
        product.name= "XYZ"
        product.base_price = 200
        product.description = "Description"
        product.category = self.create_test_category(name='xxyz')
        product.seller = self.create_test_user("userone@gmail.com").profile
        product.save()
        self.assertEqual(product.is_complete, True)

    def product_is_visible(self):
        product = self.create_test_product()
        self.assertEqual(product.is_visible, True)
        product.is_visible = False
        product.save()
        self.assertEqual(product.is_visible, False)

    def product_is_ticket(self):
        product = self.create_test_product()
        self.assertEqual(product.is_ticket, False)
        product.is_ticket = True
        product.save()
        self.assertEqual(product.is_ticket, True)

    def product_is_sold(self):
        product = self.create_test_product()
        self.assertEqual(product.is_visible, False)
        product.is_visible = True
        product.save()
        self.assertEqual(product.is_visible, True)

    def add_product_no_description(self):
        product=Product()
        is_sellable=True
        product.name= "XYZ"
        product.base_price = 20
        product.description = ""
        product.category = self.create_test_category(name='xxyz')
        product.seller = self.create_test_user("userone@gmail.com").profile
        try:
            product.save()
        except:
            is_sellable=False
        self.assertEqual(is_sellable,False)




    



    
    

        
        

    











