import boto3
import os
# produccion
acces = "AKIAY2RSPM6YLLAVMY4E"
secret = "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"
buckett= "isc-newspapers-collector"
table_name = "isc_newspapers_keywords"

# personal
# acces = "AKIAXEHO6RUC7ESHLBHA"
# secret = "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"
# buckett= "test-anytech"
# table_name = "player-points"


path = os.getcwd() + "/"

print("PATHHHH",path)


# session = boto3.Session(
#     aws_access_key_id= acces,
#     aws_secret_access_key= secret,
# )


# print("session", session)


# s3 = session.client('s3')
# print("s3", s3)


# response = s3.list_buckets()

# print("response", response)

# s3.upload_file("prueba.json", buckett, "prueba.json")


# DYNAMOOOOOOOOOOOOOOOO


dynamodb = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=acces, aws_secret_access_key=secret)
response = dynamodb.scan(TableName=table_name)

# Obtén todos los elementos del escaneo
items = response['Items']

# Itera sobre cada elemento e imprime los datos
for item in items:
    print(item)