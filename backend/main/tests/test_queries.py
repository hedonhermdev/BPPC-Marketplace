from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from main.tests.utils import execute_request_with_user
from main.auth_helpers import create_user_from_email
from main.models import *

from model_bakery import baker

from random import randint

class TestAllProductsQuery(TestCase):

    query_string = '''query{
                        products(page: 1,
                                 pagesize: 5) {
                                                page
                                                pages
                                                hasNext
                                                hasPrev
                                                objects{
                                                    name
                                                    category{
                                                        name
                                                        }
                                                    seller {
                                                        name
                                                        }
                                                    }
                                                }
                                            }'''

    def setUp(self):
        self.users = baker.make(User, _quantity=5)
        self.categories = baker.make(Category, _quantity=5)
        for i in range(5):
            product = baker.make(Product, seller = self.users[i].profile, category = self.categories[i])

    def test_user_can_get_products(self):
        user = create_user_from_email('user@marketplace.com')
        result = execute_request_with_user(self.query_string, user = user)

        self.assertNotIn('errors', result)

        data = result['data']['products']
    
        self.assertEqual(len(data["objects"]), 5)

    def test_anonymous_cannot_get_products(self):
        user = AnonymousUser()
        result = execute_request_with_user(self.query_string, user = user)

        self.assertIn('errors', result)

        error = result["errors"][0]

        self.assertEqual(error["message"], "You do not have permission to perform this action") # comparing the error message 
        

class TestAllCategoriesQuery(TestCase):

    query_string = '''query {
                        allCategories {
                            name 
                            products {
                                name
                                seller {
                                    name
                                }
                            }
                        }
                    }'''

    def setUp(self):
        self.users = baker.make(User, _quantity=5)
        self.categories = baker.make(Category, _quantity=5)
        for i in range(5):
            product = baker.make(Product, seller = self.users[i].profile, category = self.categories[i])

    def test_user_can_get_all_categories(self):
        user = create_user_from_email('anshal@marketplace.com')
        result = execute_request_with_user(self.query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['allCategories']

        self.assertEqual(len(data), 5)
        self.assertEqual(len(data[0]['products']), 1)

    def test_anonymous_cannot_get_products(self):
        user = AnonymousUser()
        result = execute_request_with_user(self.query_string, user = user)

        self.assertIn('errors', result)

        error = result["errors"][0]

        self.assertEqual(error["message"], "You do not have permission to perform this action")

class TestAllProfilesQuery(TestCase):

    query_string = '''query {
                        allProfiles {
                            name
                            products {
                                name
                            }
                            offers {
                                offerer {
                                    name
                                }
                                product {
                                    name
                                }
                                amount
                            }
                            reports {
                                reportedUser {
                                    name
                                }
                                reportedBy {
                                    name
                                }
                                category
                            }
                        }              
                    }'''

    def setUp(self):
        self.users = baker.make(User, _quantity=5)
        self.categories = baker.make(Category, _quantity=5)
        self.products = baker.make(Product, _quantity=5)

        for i in range(5):
            product = baker.make(Product, seller = self.users[i].profile, category = self.categories[i])

        for i in range(5):
            offer = baker.make(ProductOffer, offerer = self.users[i-1].profile, product = self.products[i], amount = randint(0, 10000))

        for i in range(5):
            report = baker.make(UserReport, reported_user = self.users[i].profile, reported_by = self.users[i-1].profile, category = randint(1,3))

    def test_user_can_get_all_profiles(self):
        user = create_user_from_email('anshal@marketplace.com')
        result = execute_request_with_user(self.query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['allProfiles']

        self.assertEqual(len(data), 6) # 6 because a new user was created with function create_user_from_email
    
    def test_anonymous_cannot_get_products(self):
        user = AnonymousUser()
        result = execute_request_with_user(self.query_string, user = user)

        self.assertIn('errors', result)

        error = result["errors"][0]

        self.assertEqual(error["message"], "You do not have permission to perform this action")

class TestMyProfileQuery(TestCase):

    query_string = '''query {
                        myProfile {
                            name
                            products {
                                name
                            }
                            offers {
                                offerer {
                                    name
                                }
                                product {
                                    name
                                }
                                amount
                            }
                            reports {
                                reportedUser {
                                    name
                                }
                                reportedBy {
                                    name
                                }
                                category
                            }
                        }
                    }'''

    def test_user_can_get_my_profile(self):
        user = create_user_from_email('anshal@marketplace.com')
        category = baker.make(Category, _quantity=1)
        users = baker.make(User, _quantity=1)
        product = baker.make(Product, seller = user.profile, category = category[0])
        offer = baker.make(ProductOffer, offerer = users[0].profile, product = product, amount = randint(0, 10000))
        report = baker.make(UserReport, reported_user = user.profile, reported_by = users[0].profile, category = randint(1,3))

        result = execute_request_with_user(self.query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['myProfile']

        self.assertEqual(len(data), 4)
    
    def test_anonymous_cannot_get_products(self):
        user = AnonymousUser()
        result = execute_request_with_user(self.query_string, user = user)

        self.assertIn('errors', result)

        error = result["errors"][0]

        self.assertEqual(error["message"], "You do not have permission to perform this action")