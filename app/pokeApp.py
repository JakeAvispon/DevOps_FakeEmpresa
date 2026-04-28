from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# Configuración de conexión a AWS DynamoDB
REGION = 'us-east-2'  # Región de Ohio, donde está tu tabla
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table_name = "PokemonFinance"

def obtener_datos_dynamo():
    try:
        tabla = dynamodb.Table(table_name)
        # Scan trae todos los registros de la tabla
        respuesta = tabla.scan()
        items = respuesta.get('Items', [])
        
        # DynamoDB devuelve los datos desordenados, así que los ordenamos por ID
        items_ordenados = sorted(items, key=lambda x: int(x['ID']))
        return items_ordenados
    except Exception as e:
        print(f"Error conectando a DynamoDB: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. Obtenemos los datos frescos de la Nube
    pokemon_list = obtener_datos_dynamo()
    
    resultados = pokemon_list
    busqueda = ""
    filtro_gen = "todas"
    filtro_tipo = "todos"

    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').lower()
        filtro_gen = request.form.get('generacion', 'todas')
        filtro_tipo = request.form.get('tipo', 'todos')

        filtrados = []
        for p in pokemon_list:
            # Los datos de DynamoDB vienen como diccionarios. Usamos .get() por seguridad.
            match_texto = busqueda in p.get('Nombre', '').lower() or busqueda == str(p.get('ID', ''))
            match_gen = (filtro_gen == 'todas' or str(p.get('Generacion', '')) == filtro_gen)
            
            tipo1 = p.get('Tipo1', '')
            tipo2 = p.get('Tipo2', '')
            match_tipo = (filtro_tipo == 'todos' or tipo1 == filtro_tipo or tipo2 == filtro_tipo)
            
            if match_texto and match_gen and match_tipo:
                filtrados.append(p)
                
        resultados = filtrados

    tipos_unicos = set()
    for p in pokemon_list:
        if p.get('Tipo1'): tipos_unicos.add(p['Tipo1'])
        if p.get('Tipo2'): tipos_unicos.add(p['Tipo2'])

    return render_template('index.html', 
                           resultados=resultados, 
                           busqueda=busqueda, 
                           filtro_gen=filtro_gen,
                           filtro_tipo=filtro_tipo,
                           tipos_disponibles=sorted(list(tipos_unicos)))

if __name__ == '__main__':
    # Puerto 5000 abierto para tu EC2
    app.run(host='0.0.0.0', port=5000, debug=True)