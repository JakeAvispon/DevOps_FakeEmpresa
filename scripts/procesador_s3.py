import sys
import boto3
from datetime import datetime

REGION = 'us-east-1'
BUCKET_NAME = 'tu-bucket-finanzas-pokemon-2026' # <-- ¡CÁMBIA ESTO por el nombre de tu bucket!
dynamodb = boto3.resource('dynamodb', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)

def main():
    tipo_filtro = "Fuego" # Puedes cambiarlo o pasarlo por argumentos
    table_name = "PokemonFinance"
    output_file = f"reporte_tipo_{tipo_filtro.lower()}.txt"
    
    tabla = dynamodb.Table(table_name)
    
    print(f"Buscando Pokémon de tipo {tipo_filtro} en DynamoDB...")
    respuesta = tabla.scan()
    items = respuesta.get('Items', [])
    
    datos_filtrados = [item for item in items if item.get('Tipo1') == tipo_filtro or item.get('Tipo2') == tipo_filtro]
    
    # Escribimos el .txt
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== REPORTE FINANCIERO DE POKEMON TIPO {tipo_filtro.upper()} ===\n")
        f.write(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")
        
        for pkmn in datos_filtrados:
            f.write(f"ID: {pkmn['ID']} | Nombre: {pkmn['Nombre']} | Modificado por: {pkmn.get('ModificadoPor')} a las {pkmn.get('HoraModificacion')}\n")
            
    print(f"Archivo {output_file} generado localmente. Subiendo a S3...")
    
    # Subir a S3
    try:
        s3.upload_file(output_file, BUCKET_NAME, output_file)
        print(f"¡Éxito! Archivo subido al bucket: {BUCKET_NAME}")
    except Exception as e:
        print(f"Error subiendo a S3: {e}")

if __name__ == '__main__':
    main()