import json
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError
from infraStructure.VisitorCountInfra.src.handlers.putVisitorCount import putVisitorCountHandler  


@mock_aws
def test_put_visitor_count_success():
    """
    Test case for a successful increment of the visitor count.
    """
    dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
    table_name = "VisitorCountTable"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "visitors", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "visitors", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'
    )
    table = dynamodb.Table(table_name)

    table.put_item(Item={"visitors": "visitorCount", "count": 5})

    event = {}
    context = {}
    response = putVisitorCountHandler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Visitor count incremented successfully"
    assert body["visitorCount"] == 6


@mock_aws
def test_put_visitor_count_table_not_found():
    """
    Test case when the DynamoDB table is missing.
    """
    event = {}
    context = {}
    response = putVisitorCountHandler(event, context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "error" in body
    assert "Requested resource not found" in body["error"]


@mock_aws
def test_put_visitor_count_missing_primary_key():
    """
    Test case when the table's schema does not match the request.
    """
    dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
    table_name = "VisitorCountTable"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "wrongKey", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "wrongKey", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'  

    )

    event = {}
    context = {}
    response = putVisitorCountHandler(event, context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "error" in body
    assert "The provided key element does not match the schema" in body["error"]


# @mock_aws
# def test_put_visitor_count_insufficient_permissions():
#     """
#     Test case for insufficient permissions.
#     """
#     dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
#     table_name = "VisitorCountTable"
#     dynamodb.create_table(
#         TableName=table_name,
#         KeySchema=[{"AttributeName": "visitors", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "visitors", "AttributeType": "S"}],
#         BillingMode='PAY_PER_REQUEST'  

#     )

#     # Remove permissions from the table (simulate permission error)
#     table = dynamodb.Table(table_name)
#     table.meta.client.meta.events.unregister("before-call.dynamodb", table.meta.client._sign)

#     event = {}
#     context = {}
#     response = putVisitorCountHandler(event, context)

#     assert response["statusCode"] == 500
#     body = json.loads(response["body"])
#     assert "error" in body
#     assert "not authorized" in body["error"].lower()


@mock_aws
def test_put_visitor_count_no_initial_item():
    """
    Test case when there is no initial item, and it creates a new one.
    """
    dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
    table_name = "VisitorCountTable"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "visitors", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "visitors", "AttributeType": "S"}],
        BillingMode='PAY_PER_REQUEST'  

    )

    event = {}
    context = {}
    response = putVisitorCountHandler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Visitor count incremented successfully"
    assert body["visitorCount"] == 1
