import boto3

acces = "AKIAXEHO6RUC7ESHLBHA"
secret = "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"
buckett= "test-anytech"
table_name = "player-points"


dynamodb = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=acces, aws_secret_access_key=secret)
response = dynamodb.scan(TableName=table_name)

# Obtén todos los elementos del escaneo
items = response['Items']

# Itera sobre cada elemento e imprime los datos
for item in items:
    print(item)