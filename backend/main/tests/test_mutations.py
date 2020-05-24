from django.test import RequestFactory, TestCase
from graphene.test import Client

from marketplace.schema import schema
from main.auth_helpers import create_user_from_email, get_jwt_with_user

import json

GRAPHQL_URL = '/api/graphql/'
GRAPHQL_SCHEMA = schema

def execute_mutation_with_user(query, user=None, variables=None, **kwargs):
    req = RequestFactory()
    context = req.post(GRAPHQL_URL)
    context.user = user
    client = Client(GRAPHQL_SCHEMA)
    result = client.execute(query, variables, context_value=context, **kwargs)

    return result


class TestProductMutations(TestCase):
    query_string = '''
        mutation {
            createProduct(input: {
                name: "Thomas Calculus",
                expectedPrice: 400,
                isNegotiable: false,
                description: "Never used. Mint condition.",
                })
                {
                    ok: ok
                }
        }
        '''

    def test_bitsian_can_create_product(self):
        user = create_user_from_email('f20190120@pilani.bits-pilani.ac.in')
        result = execute_mutation_with_user(self.query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['createProduct']

        self.assertEqual(data['ok'], True)

    def test_non_bitsian_cannot_make_new_product(self):
        user = create_user_from_email('jaintirth24@gmail.com')
        result = execute_mutation_with_user(self.query_string, user=user)

        self.assertIn('errors', result)

        data = result['data']['createProduct']
        self.assertIsNone(data)

    def test_product_attributes(self):
