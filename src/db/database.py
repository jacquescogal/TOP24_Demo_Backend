import aioboto3
import os


class Database:
    
    def __init__(self):
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region_name = os.getenv('AWS_REGION_NAME')
        self.session = aioboto3.Session()

    async def get_item(self, table_name, key):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.get_item(Key=key)
            return response.get('Item')
        
    async def put_item(self, table_name, item):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.put_item(Item=item)
            return response
    
    async def update_item(self, table_name, key, update_expression, expression_attribute_values):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return response
        
    async def delete_item(self, table_name, key):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.delete_item(Key=key)
            return response
        
    async def scan(self, table_name):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.scan()
            return response.get('Items')
        
    async def query(self, table_name, key_condition_expression, expression_attribute_values):
        async with self.session.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            response = await table.query(
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return response.get('Items')