import boto3
import datetime

def lambda_handler(event, context):
    ses_client = boto3.client('ses')
    # Define los detalles del correo electrónico
    sender = 'juan.lopez.de.la.plaza@alumnojoyfe.iepgroup.es'
    recipient = 'juan.lopez.de.la.plaza@alumnojoyfe.iepgroup.es'
    subject = 'Nuevo mensaje en WEB'
    body = 'Hola, hay un nuevo mensaje en su pagina WEB'

    try:
        # Verifica el remitente
        response = ses_client.verify_email_identity(EmailAddress=sender)
        print(f"Sender {sender} verification initiated")
    except Exception as e:
        print(f"Error verifying sender {sender}: {e}")
        return

    try:
        # Envía el correo electrónico
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"Email sent with MessageId: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {e}")
    # Envía el correo electrónico
    # response = ses_client.send_email(
    #     Source=sender,
    #     Destination={
    #         'ToAddresses': [recipient]
    #     },
    #     Message={
    #         'Subject': {
    #             'Data': subject
    #         },
    #         'Body': {
    #             'Text': {
    #                 'Data': body
    #             }
    #         }
    #     }
    # )

    body = event.get('body', {}).get('body')
    print(body)

    if body is not None:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        file_name = "juan.txt"

        # Obtener el contenido actual del archivo si existe
        s3_client = boto3.client('s3')
        try:
            response = s3_client.get_object(
                Bucket='texto-proyecto-3',
                Key=file_name
            )
            existing_content = response['Body'].read().decode('utf-8')
        except s3_client.exceptions.NoSuchKey:
            existing_content = ""

        # Agregar el nuevo texto al contenido existente
        updated_content = f"{existing_content}<br><br>{body}<br>--[ {formatted_time} ]--"
        print(updated_content)
        # Guardar el archivo actualizado en S3
        s3_client.put_object(
            Body=updated_content.encode('utf-8'),
            Bucket='texto-proyecto-3',
            Key=file_name
        )

        return {
            'statusCode': 200,
            'body': 'Texto agregado exitosamente al archivo en S3'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'El cuerpo de la solicitud es nulo'
        }