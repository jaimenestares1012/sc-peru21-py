import boto3
import os
# produccion
# acces = "AKIAY2RSPM6YLLAVMY4E"
# secret = "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"
# buckett= "isc-newspapers-collector"
# table_name = "isc_newspapers_keywords"





def insertAws(carpeta, nombre_archivo):
    print("<------------------>")
    print("carpeta", carpeta)
    print("nombre_archivo", nombre_archivo)
    print("<------------------>")
    # produccion
    # acces = "AKIAY2RSPM6YLLAVMY4E"
    # secret = "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"
    # buckett= "isc-newspapers-collector"

    # personal
    acces = "AKIAXEHO6RUC7ESHLBHA"
    secret = "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"
    buckett= "test-anytech"


    # path = os.getcwd() + "/"

    # print("PATHHHH",path)



    session = boto3.Session(
        aws_access_key_id= acces,
        aws_secret_access_key= secret,
    )


    print("session", session)


    s3 = session.client('s3')
    print("s3", s3)


    response = s3.list_buckets()

    print("response", response)

    s3.upload_file("data/{}/{}.json".format(carpeta, nombre_archivo), buckett, "data/{}/{}.json".format(carpeta,nombre_archivo))


# insertAws("2023-06-09","fa1ad66cfb0acc7719b38cfc503b0195")
