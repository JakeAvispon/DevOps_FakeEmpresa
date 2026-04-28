import requests
import json
import concurrent.futures
import time

traduccion_tipos = {
    "normal": "Normal", "fire": "Fuego", "water": "Agua", "electric": "Eléctrico",
    "grass": "Planta", "ice": "Hielo", "fighting": "Lucha", "poison": "Veneno",
    "ground": "Tierra", "flying": "Volador", "psychic": "Psíquico", "bug": "Bicho",
    "rock": "Roca", "ghost": "Fantasma", "dragon": "Dragón", "dark": "Siniestro",
    "steel": "Acero", "fairy": "Hada"
}

def obtener_generacion(pkmn_id):
    if pkmn_id <= 151: return 1
    elif pkmn_id <= 251: return 2
    elif pkmn_id <= 386: return 3
    elif pkmn_id <= 493: return 4
    elif pkmn_id <= 649: return 5
    elif pkmn_id <= 721: return 6
    elif pkmn_id <= 809: return 7
    elif pkmn_id <= 905: return 8
    else: return 9

def descargar_pokemon(pkmn_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pkmn_id}"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            data = respuesta.json()
            
            tipos = data['types']
            tipo1 = tipos[0]['type']['name']
            tipo2 = tipos[1]['type']['name'] if len(tipos) > 1 else None
            
            # Obtener el sprite estilo GBA (Generación III)
            gba_sprite_url = None
            try:
                versions = data.get('sprites', {}).get('versions', {})
                gen3 = versions.get('generation-iii', {})
                gba_sprite_url = gen3.get('fire-red-leaf-green', {}).get('front_default')
                if not gba_sprite_url:
                     gba_sprite_url = gen3.get('ruby-sapphire', {}).get('front_default')
                if not gba_sprite_url:
                    gba_sprite_url = data.get('sprites', {}).get('front_default')
            except:
                pass
            
            return {
                "ID": data['id'],
                "Nombre": data['name'].capitalize(),
                "Tipo1": traduccion_tipos.get(tipo1, tipo1),
                "Tipo2": traduccion_tipos.get(tipo2, tipo2) if tipo2 else None,
                "Generacion": obtener_generacion(data['id']),
                "GBA_Sprite_URL": gba_sprite_url
            }
    except:
        pass
    return None

def main():
    print("Descargando 1025 Pokémon... Esto tomará un par de minutos.")
    pokedex_completa = []
    inicio = time.time()
    
    ids_pokemon = list(range(1, 1026))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        resultados = executor.map(descargar_pokemon, ids_pokemon)
        
        for i, pkmn in enumerate(resultados):
            if pkmn:
                pokedex_completa.append(pkmn)
            if (i + 1) % 100 == 0:
                print(f"Descargados {i + 1} / 1025...")

    pokedex_completa.sort(key=lambda x: x['ID'])
    
    with open('pokemon.json', 'w', encoding='utf-8') as f:
        json.dump(pokedex_completa, f, indent=4, ensure_ascii=False)
        
    tiempo_total = round(time.time() - inicio, 2)
    print(f"\n[ÉXITO] Archivo pokemon.json generado en {tiempo_total} segundos.")

if __name__ == '__main__':
    main()