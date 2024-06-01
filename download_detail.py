import random
from astroquery.simbad import Simbad
import numpy as np
import time

# Establecer el límite de filas a 0 para obtener todos los resultados
Simbad.ROW_LIMIT = 0

# Establecer el tiempo de espera a 10 minutos
Simbad.TIMEOUT = 600

# Extend Simbad to return specific fields
Simbad.add_votable_fields('ra', 'dec', 'flux(V)', 'plx', 'otype')

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
    "YellowSG*": "Uncommon"
}

def classify_object(otype):
    return object_types.get(otype)

# Función para serializar los resultados
def serialize_result(result, obj_type):
    return {
        "name": str(result["MAIN_ID"]),
        "ra": str(result["RA"]),
        "dec": str(result["DEC"]),
        "flux(V)": str(result["FLUX_V"]) if "FLUX_V" in result.colnames and result["FLUX_V"] is not None else None,
        "parallax": str(result["PLX_VALUE"]) if "PLX_VALUE" in result.colnames and result["PLX_VALUE"] is not None else None,
        "type": obj_type,  # Usar el obj_type proporcionado
        "category": classify_object(obj_type)  # Usar el obj_type proporcionado
    }

# Variable para almacenar todos los datos
all_data = ""

# Iterar sobre cada tipo de objeto
for obj_type in object_types.keys():
    print(f"Querying for object type: {obj_type}")
    try:
        result = Simbad.query_criteria(maintypes=obj_type)
        if result:
            for row in result:
                obj_data = serialize_result(row, obj_type)
                all_data += f"{obj_data}\n"
        else:
            print(f"No data found for object type: {obj_type}")
    except Exception as e:
        print(f"Error querying object type {obj_type}: {e}")
    # Esperar un poco antes de la siguiente consulta para no sobrecargar el servidor
    time.sleep(1)

# Guardar todos los datos en un archivo
with open("simbad_data.txt", "w") as file:
    file.write(all_data)

print("Datos guardados en simbad_data.txt")
