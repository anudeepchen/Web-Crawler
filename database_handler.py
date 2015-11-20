from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key

# dynamodb = boto3.resource('dynamodb')
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='us-east-1',aws_access_key_id='any',aws_secret_access_key='key')


# dynamodb = boto3.resource('dynamodb',endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

# Table creation
def create_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'word',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'url',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'word',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'url',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'word_count',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            },
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'TopWordCountsIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'word',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'word_count',
                            'KeyType': 'RANGE'
                        },

                    ],
                    'Projection': {
                        'ProjectionType': 'ALL',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                }]
        )
        print("Table status:", table.table_status)
    except:
        table = dynamodb.Table(table_name)
        print("Table status:", table.table_status)


# Adding an item to the table
def add_item(item, table_name):
    # item={'url': url, 'word': word, 'word_count': word_count, 'hyperlinks'=['h1','h2']}
    # table_name: 'Pages'
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={'word': item['word'],
              'url': item['url'],
              'word_count': item['word_count'],
              'hyperlinks': item['hyperlinks']
              }
    )


# Query 1
# Given a url and a word, return the count for this word
def get_word_count_in_page(word, url, table_name):
    # table_name: 'Pages'
    table = dynamodb.Table(table_name)
    # TODO use get_item instead
    response = table.query(
        KeyConditionExpression=Key('url').eq(url) & Key('word').eq(word)
    )
    if response['Count'] == 0:
        return 0
    else:
        return response['Items'][0]['word_count']


# Query 2
# Given a word, get the top n urls containing that word
def get_top_urls_for_word(word, n, table_name):
    # table_name: 'Pages'
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('word').eq(word),
        IndexName='TopWordCountsIndex',
        Limit=n
    )
    return response


if __name__ == '__main__':
    table_name = 'Pages3'
    create_table(table_name)
    item = {}
    item['url'] = 'url1'
    item['word'] = 'word1'
    item['word_count'] = 15
    item['hyperlinks'] = ['hard', 'to', 'combine']
    add_item(item, table_name)

    item2 = {}
    item2['url'] = 'hard'
    item2['word'] = 'word1'
    item2['word_count'] = 16
    item2['hyperlinks'] = ['blabla', 'to', 'combine']
    add_item(item2, table_name)

    response1 = get_word_count_in_page('word1', 'url1', table_name)
    response2 = get_word_count_in_page('not_in_table', 'url1', table_name)

    print(response1)
    print(response2)

    response3 = get_top_urls_for_word('word1', 2, table_name)
    print(response3)
    print('number of results ', response3['Count'])
    print('first count', response3['Items'][0]['word_count'])
    print('second count', response3['Items'][1]['word_count'])
