import os
import boto3
from decimal import Decimal
import json
import uuid
from datetime import datetime
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.idempotency import (
    IdempotencyConfig, DynamoDBPersistenceLayer, idempotent_function
)

orders_table = os.getenv('TABLE_NAME')
idempotency_table = os.getenv('IDEMPOTENCY_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')

persistence_layer = DynamoDBPersistenceLayer(table_name=idempotency_table)
idempotency_config = IdempotencyConfig(event_key_jmespath="powertools_json(body).orderId")

@idempotent_function(data_keyword_argument="event", config=idempotency_config, persistence_store=persistence_layer)
def add_order(event: dict):
    detail = json.loads(event['body'])
    restaurant_id = detail['restaurantId']
    total_amount = detail['totalAmount']
    order_items = detail['orderItems']
    user_id = event['requestContext']['authorizer']['claims']['sub']
    order_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    order_id = detail['orderId']

    ddb_item = {
        'orderId': order_id,
        'userId': user_id,
        'data': {
            'orderId': order_id,
            'userId': user_id,
            'restaurantId': restaurant_id,
            'totalAmount': total_amount,
            'orderItems': order_items,
            'status': 'PLACED',
            'orderTime': order_time,
        }
    }
    ddb_item = json.loads(json.dumps(ddb_item), parse_float=Decimal)

    table = dynamodb.Table(orders_table)
    # We must use conditional expression, otherwise put_item will always replace the original order and will never fail
    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(orderId) AND attribute_not_exists(userId)')

    detail['orderId'] = order_id
    detail['status'] = 'PLACED'
    detail['orderTime'] = order_time

    return detail


def lambda_handler(event, context: LambdaContext):
    idempotency_config.register_lambda_context(context)
    """Handles the lambda method invocation"""
    try:
        order_detail = add_order(event=event)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(order_detail)
        }
        return response
    except Exception as err:
        raise
