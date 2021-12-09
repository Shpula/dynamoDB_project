import json
import boto3

response = []
data = []
params = {}
AWS_KEY = "********"
AWS_SECRET = "***********"
dynamodb_json = json.dumps('test')

dynamo_res = boto3.resource('dynamodb',
                            aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name='us-east-1'
                            )

table = dynamo_res.Table('bigrig-profile-dev')
doc = json.load(open('test_profile.json', 'rb'))
table.put_item(
    Item=doc
)

