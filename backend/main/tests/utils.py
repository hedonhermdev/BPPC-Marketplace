import json

from django.test import RequestFactory
from graphene.test import Client

from marketplace.schema import schema

GRAPHQL_URL = '/api/graphql/'
GRAPHQL_SCHEMA = schema

def execute_request_with_user(query, user=None, variables=None, **kwargs):
    req = RequestFactory()
    context = req.post(GRAPHQL_URL)
    context.user = user
    client = Client(GRAPHQL_SCHEMA)
    result = client.execute(query, variable_values=variables, context_value=context, **kwargs)

    return result
