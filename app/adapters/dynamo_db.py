import boto3

from app.config import ENDPOINT_URL


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    table = dynamodb.create_table(
        # TableName='AirportFinderTable',
        # KeySchema=[
        #     {
        #         'AttributeName': 'geonameid',
        #         'KeyType': 'HASH'  # Partition key
        #     },
        #     {
        #         'AttributeName': 'name',
        #         'KeyType': 'RANGE',  # Sort key
        #     }
        # ],
        # AttributeDefinitions=[
        #     {
        #         'AttributeName': 'geonameid',
        #         'AttributeType': 'N'
        #     },
        #     {
        #         'AttributeName': 'name',
        #         'AttributeType': 'S',
        #     }

        TableName='Movies',  # TODO TEMP
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


# ,geonameid,name,asciiname,country,latitude,longitude,airport

def save_item_to_dynamodb(item, table_name='AirportFinderTable', dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)
    table = dynamodb.Table(table_name)
    geonameid = int(item['geonameid'])
    name = item['name']
    print("Adding item:", geonameid, name)
    table.put_item(Item=item)


def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    table = dynamodb.Table('Movies')
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)


movie_list = [{
    "year": 2013,
    "title": "Turn It Down, Or Else!",
    "info": {
        "directors": [
            "Alice Smith",
            "Bob Jones"
        ],
        "release_date": "2013-01-18T00:00:00Z",
        "rating": 6,
        "genres": [
            "Comedy",
            "Drama"
        ],
        "image_url": "http://ia.media-imdb.com/images/N/O9ERWAU7FS797AJ7LU8HN09AMUP908RLlo5JF90EWR7LJKQ7@@._V1_SX400_.jpg",
        "plot": "A rock band plays their music at high volumes, annoying the neighbors.",
        "rank": 11,
        "running_time_secs": 5215,
        "actors": [
            "David Matthewman",
            "Ann Thomas",
            "Jonathan G. Neff"
        ]
    }
}]

if __name__ == '__main__':
    # new_table = create_table()
    # print("Table status:", new_table.table_status)
    load_movies(movie_list)
