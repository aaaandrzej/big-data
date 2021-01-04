from decimal import Decimal

import boto3

from app.config import ENDPOINT_URL
from app.core.timer import timer


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    table = dynamodb.create_table(
        TableName='AirportFinderTable',
        KeySchema=[
            {
                'AttributeName': 'geonameid',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE',  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'geonameid',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='AirportFinderTable')
    return table


def save_item_to_dynamodb(item, table_name='AirportFinderTable', output_fieldnames=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    if table_name not in [t.name for t in dynamodb.tables.all()]:
        create_table()

    if output_fieldnames:
        item = {k: item[k] for k in output_fieldnames if k in item}

    item['longitude'] = Decimal(str(item['longitude']))  # TODO dynamodb error workaround, refactor probably required
    item['latitude'] = Decimal(str(item['latitude']))

    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


@timer
def save_df_to_dynamodb(df, table_name='AirportFinderTable', output_fieldnames=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    for item in df.to_dict(orient="records"):
        save_item_to_dynamodb(item, table_name=table_name, output_fieldnames=output_fieldnames, dynamodb=dynamodb)
