import boto3

def lambda_handler(event, context):
    # Nombre del bucket
    bucket_name = 'texto-proyecto-3'

    # Conexión al cliente de S3
    s3_client = boto3.client('s3')

    # Obtener la lista de objetos en el bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Obtener el último objeto en la lista (basado en la fecha de modificación)
    last_modified_obj = max(response['Contents'], key=lambda obj: obj['LastModified'])

    # Obtener el contenido del último archivo
    file_key = last_modified_obj['Key']
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    print(file_content)
    # Devolver el contenido leído
    return file_content
