import json
from collections import Counter
import boto3

ID = "************"
response = []
data = []
brands_dict = {}
brands_list = []
trucks_dict = {}
trucks_list = []
new_brand_dict = {}
AWS_KEY = "**************"
AWS_SECRET = "**************"
dynamodb_json = json.dumps('test')

dynamo_res = boto3.resource('dynamodb',
                            aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name='us-east-1'
                            )

table = dynamo_res.Table('bigrig-profile-dev')
doc = json.load(open('google_docs_config.json', 'rb'))

response = table.get_item(
    Key={'ID': ID
         }
    , ProjectionExpression="Trucks, #i"
    , ExpressionAttributeNames={"#i": 'items'}
)

n = 0
while n < len(response['Item']['Trucks']):
    trucks_dict = (response['Item']['Trucks'][n])
    trucks_list.append(trucks_dict)
    n += 1

x_brand = {t['ConfigKey']: t['Brand'] for t in doc['Trucks']}
print(x_brand)

for t in trucks_list:
    t["Brand"] = new_brand_dict[t["ConfigKey"]]

temp_items = {}
index_trucks_list = []
another_index_trucks_list = []
another_dict = []
n = -1
for items in trucks_list:
    n += 1
    index_trucks_list.append(n)
    for item in list(items["items"]):
        if item.split("_")[0] != items["Brand"].lower():
            temp_items.update({item: items["items"][item]})
            another_index_trucks_list.append(temp_items.copy())
            another_dict.append(temp_items.copy())
            index_trucks_list.append(temp_items.copy())
            temp_items.clear()
            del items["items"][item]

test_curr_dict = {}
for i in another_dict:
    test_curr_dict.update(i)


lists = [Counter(d) for d in another_index_trucks_list]
result = Counter()
for d in lists:
    result += d

another_index_trucks_list_key = []
another_index_trucks_list_values = []

items = result.items()
for item in items:
    another_index_trucks_list_key.append(item[0]), another_index_trucks_list_values.append(item[1])

main_items_dict = {}
main_items_dict.update(response["Item"]["items"])
main_item_values = []
main_item_key = []
main_item_key, main_item_values = zip(*main_items_dict.items())

test_set = list(set({}))
number = 0
contains_str = ''
for i in range(len(index_trucks_list)):
    if type(index_trucks_list[i]) == int:
        number = index_trucks_list[i]
    else:
        test_set.append(*index_trucks_list[i].values())
        contains_str += f"(Trucks[{number}].#i.{next(iter(index_trucks_list[i].keys()))} = :{next(iter(index_trucks_list[i].values()))}) AND "
contains_str = contains_str.rstrip(' AND ')

currect_tuid = {}
n = 0
for i in response["Item"]["Trucks"]:
    currect_tuid.update({f":tuid{n}": i["TUID"]})
    n += 1

tuid_str = ""
n = -1
for i in currect_tuid:
    n += 1
    tuid_str += f"Trucks[{n}].TUID = {i} AND "
tuid_str = tuid_str.rstrip(' AND ')

add_str = "ADD "
for k, v in zip(another_index_trucks_list_key, another_index_trucks_list_values):
    add_str += f'#i.{k}' + f' :{v}, '
add_str = add_str.rstrip(', ')

number = 0
remove_str = 'REMOVE '
for i in range(len(index_trucks_list)):
    if type(index_trucks_list[i]) == int:
        number = index_trucks_list[i]
    else:
        remove_str += f"Trucks[{number}].#i.{next(iter(index_trucks_list[i].keys()))}, "
remove_str = remove_str.rstrip(', ')
final_str = remove_str + " " + add_str

set_temp_values = list(set(another_index_trucks_list_values))
str_list = list(map(str, set_temp_values))
str_list_another = list(map(str, test_set))
str_list_final = str_list + str_list_another
set_temp_final = set_temp_values + test_set

temp = []
for x in set_temp_final:
    if x not in temp:
        temp.append(x)
set_temp_final = temp

temp = []
for x in str_list_final:
    if x not in temp:
        temp.append(x)
str_list_final = temp

new_str_list = []
for x in str_list_final:
    new_str_list.append(f":{x}")

map_test = map(lambda *args: args, new_str_list, set_temp_final)
currect_dict = dict(map_test)

currect_dict.update(currect_tuid)

response = table.update_item(
    Key={
        'ID': ID
    }
    , ConditionExpression=f"{contains_str}" + " AND " + f"{tuid_str}"
    , UpdateExpression=final_str

    , ExpressionAttributeNames={
        "#i": "items"
    }
    , ExpressionAttributeValues=currect_dict
)


