from django.test import TestCase

from main.models import User, Profile, ProfileRating
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
