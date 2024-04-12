import json
import firebase_admin
from firebase_admin import credentials, storage
import os

# Credenciales de Firebase
firebase_credentials = {
    "type": "service_account",
    "project_id": "ventura-bfe66",
    "private_key_id": "39983ffe5cd1631b5491c2023d2f9a4b2938a6c4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDLfihlTQVmyXmc\n2ZrDSYzWKTdMOuC/8g7e73ecmZy4+DeW5XezVgO77jNS2Ax4VaxsiaEe6LPvdxaj\ndcOhyFQY1AAy5LkhZyVzE/60eChW7Enh5nTn/gPcgdJSCt0vtKcgHbXq7J/aDFgn\nIzA90XhSBLcYw5BnuquS2w+26ZVteMmfV3c8KcuH2vOmrDsLqpFi6ubW86XiNP+q\nQ7W5Se+czXHkqnlsB3PwiQB5+0uHm1EuYQa/E18cuiVfRl2xhA4alvczGUTHeqG0\n17gLTJSV8olxUCSEHOLVEks+o2ILovKYNdT6srCFZ0IkL6rEQfkbXYkwexz1yMmJ\nnhZ1ayKpAgMBAAECggEAA4TmIzFYrHFDyYUAXov3M+1wy8BRanRf0jZrN8G20oKV\naIZFoov0YtPA3rgGiC64HYToTMnqsbOaKD/FPzchEDBbZAXtVzDq1oGEJEAXN4Cc\n2vuiri/oBnBW0C0oq9ZolP86igpnTcysmhmrUAhfN7Dl7zdTmB2j8bVY4VmLCGJ4\nVt11o2QLJBR7R+ur4vTORuYutPWDJBj4550LdRNz0UR35wsiNGWjzi5pOJjWjKMT\nS8t5VZWJ5Myu9JstTZVLxA4om+ZdILOYerRCgyUarCZUtsNlak0AJyKnBFRiCJdG\n6Mp7nR0tvAmu6iXZJpBqS+OfbPQebOG884ybIE3bMQKBgQDxvEhekv6rswIDZ+zE\n3IdwNpTso84RBuQmRW2OOHWvZxuuoQoJH86eyPUjqN46KR8vl5Fy6jiIQpPi4gFL\npxXnKiVCMAUCOfo13alub85EJ8Mc5/hlkb8I//wJ2WbP0/7FS93T+xVPrMfUc540\njzs4Ta7snG3sOseY0KckRpoMOQKBgQDXgCvsOcWAiLp6FB/7Ttt5jny/TKY47ezC\nHAgkJPJt19XrsWSyBSnLZdA/3F2bRVQGg3dCgPFugbPMAmu+YV6SmhB810QGrm3G\nJpP3d5wO0ChIhDxYuPUHD6kYfPKg2T2S12v8r10J1fWGhH3bMVAUrNXtZVBUnbeQ\nmP2R1vSp8QKBgQCr468uGKYgXyxaUaapoQppf1ZMInof31+R2yJ406rTK6Uien5R\nWJ2qiMjPL3+9qYn0ZHlXVjcWpQjVdtFnAwtvEafmtZCKMcG6VcDpt3TbP87cmhIl\n3woREz0bn8wckekCT90Po+VWf0ykxAXF5+c7NPniY6VCKdXN0uhWwiE9+QKBgDSP\n9aajnLGyJ9G48OgKHuwyPeknF/AQ0Eu0LKQsQtlZ6LqZRRdKvRv4VGgPJuHFci44\niLE25CxxBFrBSGhiNYAKhfT9SIFcsDfBlxuoF+9hBEJTxqhZTKKRRkxLxZ5H/oW/\nd35lg4rvnfhWfqAlEgRI99D0gjhxU6G4PzkANiLxAoGANeIZv/SNbNUEsrfYFQtT\n1lLN1tYVor2FrqyBrjs6Hl/KX0VRah/2jf8Ist3SH2IScEOisMhYSCB1casEQJ+/\nRF9p5aiRnWu4bSUGPBn5WYdNnFkdnKxnhNoyYdtvUTqLmcsBtIUJbU3MxUVFqX0l\nMWTM5n1dyqg3+zqr+fW+Y/U=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-54br6@ventura-bfe66.iam.gserviceaccount.com",
    "client_id": "107896651163926644005",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-54br6%40ventura-bfe66.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Configurar las credenciales de Firebase
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {'storageBucket': 'gs://ventura-bfe66.appspot.com'})

def process_files(bucket):
    # Diccionario para almacenar los conteos por edificio
    conteos_por_edificio = {}
    
    # Obtener la lista de objetos en el bucket
    blobs = bucket.list_blobs()
    
    # Iterar sobre los objetos y procesar cada archivo
    for blob in blobs:
        # Obtener el nombre del archivo
        filename = blob.name
        
        # Ignorar el archivo "edificios.json"
        if filename == "edificios.json":
            continue
        
        # Descargar el archivo JSON
        blob_content = blob.download_as_string()
        json_data = json.loads(blob_content)
        
        # Iterar sobre los conteos en el archivo JSON
        for edificio, conteo in json_data.items():
            # Actualizar el conteo del edificio
            conteos_por_edificio[edificio] = conteos_por_edificio.get(edificio, 0) + conteo
    
    return conteos_por_edificio




def top_3_edificios(conteos_por_edificio):
    # Ordenar los edificios por la cantidad de visitas (valores) en orden descendente
    top_edificios = sorted(conteos_por_edificio.items(), key=lambda x: x[1], reverse=True)
    
    # Seleccionar los tres primeros edificios del top
    top_3_edificios = top_edificios[:3]
    
    return top_3_edificios


# Inicializar el cliente de almacenamiento de Firebase

bucket = storage.bucket("ventura-bfe66.appspot.com")

    
# Procesar los archivos y obtener los conteos por edificio
conteos_por_edificio = process_files(bucket)
top_3 = top_3_edificios(conteos_por_edificio)
    
print("Conteos por edificio:", conteos_por_edificio)
print("Top edificios más visitados:", top_3)

