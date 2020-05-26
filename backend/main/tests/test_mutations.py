from django.test import RequestFactory, TestCase
from graphene.test import Client

from marketplace.schema import schema
from main.auth_helpers import create_user_from_email, get_jwt_with_user, create_product_from_email
from main.models import UserReport

import json

GRAPHQL_URL = '/api/graphql/'
GRAPHQL_SCHEMA = schema

def execute_mutation_with_user(query, user=None, variables=None, **kwargs):
    req = RequestFactory()
    context = req.post(GRAPHQL_URL)
    context.user = user
    client = Client(GRAPHQL_SCHEMA)
    result = client.execute(query, variable_values=variables, context_value=context, **kwargs)

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

    # def test_product_attributes(self):
    #     user = create_user_from_email('jaintirth24@gmail.com')
    #     result = execute_mutation_with_user(self.query_string, user=user)

class TestUserReportMutations(TestCase):
    query_string = '''
        mutation ($reportedUserName : String!){
            createUserReport(input: {
                reportedUser : $reportedUserName,
                category: 2
            }) 
                {
                    ok: ok
                }
        }
        ''' 

    def test_bitsian_can_report_bitsian(self):
        user1 = create_user_from_email('f20190663@pilani.bits-pilani.ac.in')
        user2 = create_user_from_email('f20190120@pilani.bits-pilani.ac.in')

        result = execute_mutation_with_user(self.query_string, user=user1, variables={"reportedUserName":user2.username})

        self.assertNotIn('errors', result)

        data = result['data']['createUserReport']

        self.assertEqual(data['ok'], True)

    def test_bitsian_can_report_non_bitsian(self):
        user1 = create_user_from_email('f20190663@pilani.bits-pilani.ac.in')
        user2 = create_user_from_email('darshmishra3010@gmail.com')

        result = execute_mutation_with_user(self.query_string, user=user1, variables={"reportedUserName":user2.username})

        self.assertNotIn('errors', result)
        data = result['data']['createUserReport']

        self.assertEqual(data['ok'], True)
    
    def test_non_bitsian_can_report_bitsian(self):
        user1 = create_user_from_email('darshmishra3010@gmail.com')
        user2 = create_user_from_email('f20190120@pilani.bits-pilani.ac.in')

        result = execute_mutation_with_user(self.query_string, user=user1, variables={"reportedUserName":user2.username})

        self.assertNotIn('errors', result)

        data = result['data']['createUserReport']

        self.assertEqual(data['ok'], True)

    def test_non_bitsian_can_report_non_bitsian(self):
        user1 = create_user_from_email('jaintirth24@gmail.com')
        user2 = create_user_from_email('darshmishra3010@gmail.com')

        result = execute_mutation_with_user(self.query_string, user=user1, variables={"reportedUserName":user2.username})

        self.assertNotIn('errors', result)

        data = result['data']['createUserReport']

        self.assertEqual(data['ok'], True)

    def test_number_report_increase(self):
        user1 = create_user_from_email('jaintirth24@gmail.com')
        user2 = create_user_from_email('darshmishra3010@gmail.com')

        reports = UserReport.objects.count()

        result = execute_mutation_with_user(self.query_string, user=user1, variables={"reportedUserName":user2.username})

        new_reports = UserReport.objects.count()

        self.assertNotIn('errors', result)
        self.assertEqual(reports+1,new_reports)
        data = result['data']['createUserReport']

        self.assertEqual(data['ok'], True)


class TestOfferMutations(TestCase):
    def generate_query_string(self, with_amount=True, is_negotiable=True):
        product, seller = create_product_from_email('seller@pilani.bits-pilani.ac.in', is_negotiable=is_negotiable)
        if (with_amount):
            query_string = '''mutation{
                                createOffer(productId: %d
  						                input:{
                                        amount:20000
                                        message: "mai sab kharidega"
                                        })
                                    {
                                        errors: errors
                                        ok: ok
                                    }
                            }''' % (product.id)
        else:
            query_string = '''mutation{
                                createOffer(productId: %d
  						                input:{
                                        message: "mai sab kharidega"
                                        })
                                    {
                                        errors: errors
                                        ok: ok
                                    }
                            }''' % (product.id)

        return query_string, seller

    def test_user_can_offer(self):
        query_string, _ = self.generate_query_string(with_amount=True, is_negotiable=True)
        user = create_user_from_email('buyer@xyz.in')
        result = execute_mutation_with_user(query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['createOffer']
        self.assertEqual(data['ok'], True)

    def test_user_can_offer_for_expected_price(self):
        query_string, _ = self.generate_query_string(with_amount=False, is_negotiable=False)
        user = create_user_from_email('buyer@xyz.in')
        result = execute_mutation_with_user(query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['createOffer']
        self.assertEqual(data['ok'], True)

    def test_user_cannot_make_offer_on_their_product(self):
        query_string, user = self.generate_query_string(with_amount=True, is_negotiable=True)
        result = execute_mutation_with_user(query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['createOffer']
        self.assertEqual(data['ok'], False)
        
        errors = data['errors']
        self.assertEqual(errors[0], "User cannot offer on their own product") #Matching the error message returned from mutation.

    def test_user_cannot_make_multiple_offers(self):
        query_string, _ = self.generate_query_string(with_amount=True, is_negotiable=True)
        user = create_user_from_email('buyer@xyz.in')
        result1 = execute_mutation_with_user(query_string, user=user)

        #running the same mutation again
        result2 = execute_mutation_with_user(query_string, user=user)

        self.assertNotIn('errors', result2)

        data = result2['data']['createOffer']
        self.assertEqual(data['ok'], False)

        errors = data['errors']
        self.assertEqual(errors[0], "You cannot create multiple offers")

    def test_user_cannot_make_offer_without_amount(self):
        query_string, _ = self.generate_query_string(with_amount=False, is_negotiable=True)
        user = create_user_from_email('buyer@xyz.in')
        result = execute_mutation_with_user(query_string, user=user)

        self.assertNotIn('errors', result)

        data = result['data']['createOffer']
        self.assertEqual(data['ok'], False)

        errors = data['errors']
        self.assertEqual(errors[0], "Missing argument 'amount'")
