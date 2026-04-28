import boto3
import json
import time
from datetime import datetime
from botocore.exceptions import ClientError

REGION = 'us-east-1' # <-- Cambia esto a tu región de AWS
dynamodb = boto3.resource('dynamodb', region_name=REGION)
client = boto3.client('dynamodb', region_name=REGION)
table_name = "PokemonFinance"

def cargar_datos_pokemon():
    # 1. Crear la tabla si no existe
    try:
        print(f"Verificando tabla '{table_name}'...")
        client.create_table(
            TableName=table_name,
            AttributeDefinitions=[{'AttributeName': 'ID', 'AttributeType': 'N'}],
            KeySchema=[{'AttributeName': 'ID', 'KeyType': 'HASH'}], # ID será nuestra llave primaria
            BillingMode='PAY_PER_REQUEST'
        )
        print("Creando tabla... Esperando a que esté activa...")
        waiter = client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print("Tabla activa y lista.")
    except client.exceptions.ResourceInUseException:
        print("La tabla ya existe. Procediendo a la carga.")

    tabla = dynamodb.Table(table_name)
    ahora = datetime.now()

    # 2. Leer el JSON y cargar
    try:
        print("Leyendo pokemon.json...")
        with open("pokemon.json", "r", encoding='utf-8') as f:
            datos_json = json.load(f)
            
            # Cargamos solo 50 elementos para hacer la prueba rápida (cumple el requisito)
            for entrada in datos_json[:50]: 
                
                # Mapeo del JSON integrando los atributos de auditoría solicitados
                item = {
                    "ID": entrada["ID"],
                    "Nombre": entrada["Nombre"],
                    "Tipo1": entrada["Tipo1"],
                    "Generacion": entrada["Generacion"],
                    "NuevoAtributo": "Validado", # Requisito: Agregar nuevos atributos
                    "ModificadoPor": "Pipeline_Admin", # Requisito: Quien hizo el cambio
                    "FechaModificacion": ahora.strftime("%Y-%m-%d"), # Requisito: Cuando
                    "HoraModificacion": ahora.strftime("%H:%M:%S")   # Requisito: Hora
                }
                
                # Si tiene tipo 2, lo agregamos
                if entrada.get("Tipo2"):
                    item["Tipo2"] = entrada["Tipo2"]

                tabla.put_item(Item=item)
                print(f"Cargado en DB: {item['Nombre']} (ID: {item['ID']})")

        print("\n¡Misión cumplida! Base de datos de Pokémon lista y auditada.")

    except FileNotFoundError:
        print("Error: No se encontró 'pokemon.json'. Ejecutar primero 'python scripts/pokeGenerator.py'")

if __name__ == "__main__":
    cargar_datos_pokemon()