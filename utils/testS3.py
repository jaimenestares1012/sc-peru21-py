import boto3


def insertS3(carpeta, nombre_archivo):
    try:
        acces = "AKIAXEHO6RUC6XMSTD33"
        secret = "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"
        buckett= "test-anytech"
        session = boto3.Session(
            aws_access_key_id= acces,
            aws_secret_access_key= secret,
        )
        s3 = session.client('s3')
        s3.list_buckets()
        print("s3.list_buckets()", s3.list_buckets())
        s3.upload_file("data/{}/{}.json".format(carpeta, nombre_archivo), buckett, "data/{}/{}.json".format(carpeta,nombre_archivo))
    except:
        print("ERROR SUBIR ARCHIVO" )


insertS3("2023-06-09","fa1ad66cfb0acc7719b38cfc503b0195")
