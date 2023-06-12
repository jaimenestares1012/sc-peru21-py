import boto3
# produccion
# acces = "AKIAY2RSPM6YLLAVMY4E"
# secret = "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"
# buckett= "isc-newspapers-collector"
# table_name = "isc_newspapers_keywords"

def insertS3(carpeta, nombre_archivo):
    try:
        acces = "AKIAXEHO6RUCY7NO3FF6"
        secret = "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"
        buckett= "test-anytech"
        session = boto3.Session(
            aws_access_key_id= acces,
            aws_secret_access_key= secret,
        )
        s3 = session.client('s3')
        s3.list_buckets()
        s3.upload_file("data/{}/{}.json".format(carpeta, nombre_archivo), buckett, "data/{}/{}.json".format(carpeta,nombre_archivo))
    except:
        print("ERROR SUBIR ARCHIVO" )


# insertS3("2023-06-09","fa1ad66cfb0acc7719b38cfc503b0195")
