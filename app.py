import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Probabilidades de categorías
probabilities = {
    "Common": 0.70,
    "Uncommon": 0.10,  
    "Rare": 0.05,       
    "Very Rare": 0.02,  
    "Epic": 0.001,
    "Legendary": 0.005,
    "Mythical": 0.001,
    "Cosmic": 0.0001
}

# Object types classification
object_types = {
    "Planet": "Common",
    "BrownD*": "Uncommon",
    "Maser": "Uncommon",
    "SuperClG": "Legendary",
    "GroupG": "Epic",
    "Compact_Gr_G": "Epic",
    "ClG": "Very Rare",
    "BH": "Mythical",
    "Ae*": "Uncommon",
    "AGB*": "Uncommon",
    "BClG": "Uncommon",
    "Be*": "Rare",
    "BLLac": "Very Rare",
    "Blazar": "Very Rare",
    "BlueCompG": "Rare",
    "BlueSG*": "Rare",
    "BlueStraggler": "Very Rare",
    "C*": "Very Rare",
    "CataclyV*": "Uncommon",
    "Cl*": "Common",
    "DkNeb": "Legendary",
    "EB*": "Uncommon",
    "EllipVar": "Uncommon",
    "HVCld": "Uncommon",
    "HV*": "Rare",
    "Neutron*": "Mythical",
    "OH/IR": "Uncommon",
    "Pec*": "Rare",
    "PN": "Rare",
    "PulsV*": "Uncommon",
    "Pulsar": "Mythical",
    "QSO": "Legendary",
    "RedSG*": "Uncommon",
    "Seyfert": "Rare",
    "SN": "Very Rare",
    "SNR": "Epic",
    "Stream*": "Epic",
    "Symbiotic*": "Very Rare",
    "Unknown": "Mythical",
    "Void": "Cosmic",
    "WD*": "Uncommon",
    "YellowSG*": "Uncommon",
    "Star": "Common",
    "Galaxy": "Common",
    "Quasar": "Rare",
    "Nebula": "Uncommon",
    "Cluster": "Rare"
}

# Object types for solar system bodies
object_types_solar_system = {
    "Star": "Mythical",
    "Planet": "Legendary",
    "Dwarf Planet": "Epic",
    "Asteroid": "Legendary",
    "Comet": "Epic",
    "Moon": "Legendary"
}

# Descripción de columnas para cada catálogo
catalogue_columns = {
    'lqac5': ["ID", "RA", "DEC", "Magnitude", "Redshift", "Type"],
    'ucac4': ["ID", "RA", "DEC", "Proper Motion RA", "Proper Motion DEC", "Magnitude"],
    'hipparcos': ["ID", "RA", "DEC", "Parallax", "Proper Motion RA", "Proper Motion DEC", "Magnitude"],
    'sdss12': ["RA_ICRS", "DE_ICRS", "class", "objID", "SDSS12", "ObsDate", "Q", "zsp", "e_zsp", "zph", "e_zph", "<zph>", "spType", "spCl"],
    'glimpse': ["ID", "Glon", "Glat", "RAJ2000", "DEJ2000", "Jmag", "Hmag", "Kmag", "3_6mag", "4_5mag", "5_8mag", "8_0mag"],
    'gaia2': ["ID", "RA", "DEC", "Parallax", "Proper Motion RA", "Proper Motion DEC", "Magnitude"],
    'gaia3': ["ID", "RA", "DEC", "Parallax", "Proper Motion RA", "Proper Motion DEC", "Magnitude"],
    'dfgrs2': ["ID", "RA", "DEC", "Redshift", "Magnitude"],
    'glade2': ["ID", "RA", "DEC", "Redshift", "Magnitude", "Type"]
}

# Cargar datos de los archivos en memoria
data = {}
simbad_data = []
solar_system_data = []

def load_data():
    global data, simbad_data, solar_system_data
    catalogue_dir = 'catalogue_data'
    for filename in os.listdir(catalogue_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(catalogue_dir, filename), 'r') as f:
                lines = f.readlines()[1:]  # Ignorar la primera línea
                key = filename.split('.')[0]
                data[key] = [line.strip() for line in lines if line.strip()]
    
    # Cargar datos de simbad_data.txt
    with open("simbad_data.txt", 'r') as f:
        simbad_data = [line.strip() for line in f.readlines()]
    
    # Cargar datos de solar_system.txt
    with open("solar_system.txt", 'r') as f:
        solar_system_data = eval(f.read())["bodies"]

def classify_object(otype):
    return object_types.get(otype)

def generate_unique_id(catalogue, line_data, line_index):
    if catalogue in ['glimpse', 'glade2', 'sdss12']:
        if catalogue == 'glimpse':
            base_id = line_data[1] if line_data[1] else "GLIMPSE"
        elif catalogue == 'glade2':
            base_id = "GLADE"
        elif catalogue == 'sdss12':
            base_id = line_data[3] if line_data[3] else "SDSS12"
        return f"{base_id}_{line_index + 1}"
    return line_data[0]

def get_random_object(category):
    if category in ["Epic", "Legendary", "Mythical"]:
        if random.random() < 0.5:  # 50% probabilidad de seleccionar un objeto dentro del sistema solar
            obj_type = random.choice(list(object_types_solar_system.keys()))
            objects = [obj for obj in solar_system_data if obj["bodyType"] == obj_type]
            if objects:
                selected_object = random.choice(objects)
                # Ajustar la categoría solo si la categoría original es Mythical
                if category == "Mythical" and (selected_object["englishName"] == "Earth" or selected_object["englishName"] == "Sun"):
                    return {"type": obj_type, "category": category, "object": selected_object}
                return {"type": obj_type, "category": object_types_solar_system[obj_type], "object": selected_object}
        else:  # 50% probabilidad de seleccionar un objeto fuera del sistema solar
            object_types_in_category = [otype for otype, cat in object_types.items() if cat == category]
            obj_type = random.choice(object_types_in_category)
            objects = [obj for obj in simbad_data if f"'type': '{obj_type}'" in obj]
            if objects:
                return {"type": obj_type, "category": category, "object": random.choice(objects)}
    else:
        # Filtrar tipos de objetos por categoría
        object_types_in_category = [otype for otype, cat in object_types.items() if cat == category]
        obj_type = random.choice(object_types_in_category)
        
        # Filtrar datos de Simbad por tipo de objeto
        objects = [obj for obj in simbad_data if f"'type': '{obj_type}'" in obj]
        if objects:
            return {"type": obj_type, "category": category, "object": random.choice(objects)}
        else:
            # Si no hay objetos en Simbad, elegir un catálogo aleatorio
            catalogue = random.choice(list(data.keys()))
            line = random.choice(data[catalogue])
            columns = catalogue_columns[catalogue]
            line_data = line.split(",")

            # Generar un identificador único para los datos sin identificador
            line_index = data[catalogue].index(line)
            unique_id = generate_unique_id(catalogue, line_data, line_index)
            line_data[0] = unique_id
            
            object_data = {columns[i]: line_data[i] for i in range(len(columns))}
            return {"type": obj_type, "category": category, "object": object_data}

def get_object_name(obj_type, obj_data):
    type_names = {
    "Planet": "Planet",
    "BrownD*": "Brown Dwarf",
    "Maser": "Maser",
    "SuperClG": "Supercluster of Galaxies",
    "GroupG": "Group of Galaxies",
    "Compact_Gr_G": "Compact Group of Galaxies",
    "ClG": "Cluster of Galaxies",
    "BH": "Black Hole",
    "Ae*": "Young Star",
    "AGB*": "Asymptotic Giant Branch Star",
    "BClG": "Brightest Cluster Galaxy",
    "Be*": "Be Star",
    "BLLac": "BL Lac Object",
    "Blazar": "Blazar",
    "BlueCompG": "Blue Compact Galaxy",
    "BlueSG*": "Blue Supergiant",
    "BlueStraggler": "Blue Straggler Star",
    "C*": "Carbon Star",
    "CataclyV*": "Cataclysmic Variable Star",
    "Cl*": "Star Cluster",
    "DkNeb": "Dark Nebula",
    "EB*": "Eclipsing Binary",
    "EllipVar": "Ellipsoidal Variable Star",
    "HVCld": "High Velocity Cloud",
    "HV*": "High Velocity Star",
    "Neutron*": "Neutron Star",
    "OH/IR": "OH/IR Star",
    "Pec*": "Peculiar Star",
    "PN": "Planetary Nebula",
    "PulsV*": "Pulsating Variable Star",
    "Pulsar": "Pulsar",
    "QSO": "Quasar",
    "RedSG*": "Red Supergiant",
    "Seyfert": "Seyfert Galaxy",
    "SN": "Supernova",
    "SNR": "Supernova Remnant",
    "Stream*": "Stellar Stream",
    "Symbiotic*": "Symbiotic Star",
    "Unknown": "Unknown Object",
    "Void": "Cosmic Void",
    "WD*": "White Dwarf",
    "YellowSG*": "Yellow Supergiant",
    "Star": "Star",
    "Galaxy": "Galaxy",
    "Quasar": "Quasar",
    "Nebula": "Nebula",
    "Cluster": "Cluster"
    }
    type_name = type_names.get(obj_type, obj_type)
    obj_id = obj_data.get("englishName") or obj_data.get("name") or obj_data.get("ID") or obj_data.get("objID") or "Unknown"
    return f"{type_name} {obj_id}"

@app.route('/rng', methods=['GET'])
def rng():
    category = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    obj = get_random_object(category)
    
    if isinstance(obj["object"], str):  # Caso simbad_data
        obj_data = eval(obj["object"])
        obj_name = get_object_name(obj_data["type"], obj_data)
        return jsonify({
            "type": obj_data["type"],
            "object": obj_data,
            "category": obj_data["category"],
            "name": obj_name
        })
    else:  # Caso catalogue_data o sistema solar
        obj_name = get_object_name(obj["type"], obj["object"])
        return jsonify({
            "type": obj["type"],
            "object": obj["object"],
            "category": obj["category"],
            "name": obj_name
        })

if __name__ == '__main__':
    load_data()
    app.run(host='0.0.0.0', port=5000)
