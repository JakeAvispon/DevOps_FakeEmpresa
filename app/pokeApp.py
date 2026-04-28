from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon_list = []
    
    if os.path.exists('pokemon.json'):
        with open('pokemon.json', 'r', encoding='utf-8') as f:
            pokemon_list = json.load(f)

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
            match_texto = busqueda in p['Nombre'].lower() or busqueda == str(p['ID'])
            match_gen = (filtro_gen == 'todas' or str(p['Generacion']) == filtro_gen)
            match_tipo = (filtro_tipo == 'todos' or p['Tipo1'] == filtro_tipo or p['Tipo2'] == filtro_tipo)
            
            if match_texto and match_gen and match_tipo:
                filtrados.append(p)
                
        resultados = filtrados

    tipos_unicos = set()
    for p in pokemon_list:
        tipos_unicos.add(p['Tipo1'])
        if p['Tipo2']: tipos_unicos.add(p['Tipo2'])

    return render_template('index.html', 
                           resultados=resultados, 
                           busqueda=busqueda, 
                           filtro_gen=filtro_gen,
                           filtro_tipo=filtro_tipo,
                           tipos_disponibles=sorted(list(tipos_unicos)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)