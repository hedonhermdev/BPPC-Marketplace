from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from main.tests.utils import execute_request_with_user
from main.auth_helpers import create_user_from_email
from main.models import Product, User, Category

from model_bakery import baker

class TestAllProductsQueries(TestCase):

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
        

class TestAllCategoriesQueries(TestCase):

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
        print('/n')
        print(data)
        self.assertEqual(len(data), 5)
        self.assertEqual(len(data[0]['products']), 1)

    def test_anonymous_cannot_get_products(self):
        user = AnonymousUser()
        result = execute_request_with_user(self.query_string, user = user)

        self.assertIn('errors', result)

        error = result["errors"][0]

        self.assertEqual(error["message"], "You do not have permission to perform this action")