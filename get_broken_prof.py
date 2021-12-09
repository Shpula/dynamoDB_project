import json
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
import boto3

brands_list = []
response = []
data = []
params = {}
AWS_KEY = "AKIAYVTEONBYJNT4D6YS"
AWS_SECRET = "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"

dynamo_res = boto3.resource('dynamodb',
                            aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name='us-east-1'
                            )
scan_kwargs = {
        'FilterExpression': Attr("Trucks").eq("Гачимен"),
        'ProjectionExpression': "#yr, title, info.rating",
        'ExpressionAttributeNames': {"#yr": "year"}
}
table = dynamo_res.Table('bigrig-profile-dev')
doc = json.load(open('google_docs_config.json', 'rb'))

a = 0
while a < len((doc['Trucks'])):
    brands_dict = (doc['Trucks'][a])
    del brands_dict["Tier"]
    brands_list.append(brands_dict)
    a += 1


params = {}
while True:
    response = table.scan(**params
                          , FilterExpression=Attr("Trucks").exists()
                          , ProjectionExpression="ID, Trucks"
                          # , ExpressionAttributeNames={"#i": 'items'}
                          )
    data.append(response['Items'])
    test = ""
    for i in data:
        test += f"{data} "
    data.clear()
    if 'LastEvaluatedKey' not in response:
        break
    else:
        params = {"ExclusiveStartKey": response['LastEvaluatedKey']}

print(test)
