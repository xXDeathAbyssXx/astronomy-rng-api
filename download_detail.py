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
    "Planet": "Common",  # Planeta
    "BrownD*": "Uncommon",  # Enanas marrones
    "Maser": "Uncommon",  # Maser
    "SuperClG": "Legendary",  # Supercúmulo de galaxias
    "GroupG": "Epic",  # Grupo de galaxias
    "Compact_Gr_G": "Epic",  # Grupo compacto de galaxias
    "ClG": "Very Rare",  # Cúmulo de galaxias
    "BH": "Epic",  # Agujero negro
    "Ae*": "Uncommon",  # Estrella joven
    "AGB*": "Uncommon",  # Estrella en la rama asintótica gigante
    "BClG": "Uncommon",  # Galaxia más grande en un cúmulo
    "Be*": "Rare",  # Estrella con disco espectral
    "BLLac": "Very Rare",  # Galaxia activa tipo BL Lac
    "Blazar": "Very Rare",  # Blazar
    "BlueCompG": "Rare",  # Galaxia azul compacta
    "BlueSG*": "Rare",  # Supergigante azul
    "BlueStraggler": "Very Rare",  # Estrella rezagada azul
    "C*": "Very Rare",  # Estrella de carbono
    "CataclyV*": "Uncommon",  # Estrella cataclísmica variable
    "Cl*": "Common",  # Cúmulo estelar
    "DkNeb": "Legendary",  # Nebulosa oscura
    "EB*": "Uncommon",  # Binaria eclipsante
    "EllipVar": "Uncommon",  # Estrella variable elipsoidal
    "HVCld": "Uncommon",  # Nube de alta velocidad
    "HV*": "Rare",  # Estrella de alta velocidad
    "Neutron*": "Legendary",  # Estrella de neutrones
    "OH/IR": "Uncommon",  # Estrella OH/IR
    "Pec*": "Rare",  # Estrella peculiar
    "PN": "Rare",  # Nebulosa planetaria
    "PulsV*": "Uncommon",  # Estrella variable pulsante
    "Pulsar": "Legendary",  # Púlsar
    "QSO": "Legendary",  # Cuásar
    "RedSG*": "Uncommon",  # Supergigante roja
    "Seyfert": "Rare",  # Galaxia Seyfert
    "SN": "Very Rare",  # Supernova
    "SNR": "Epic",  # Remanente de supernova
    "Stream*": "Epic",  # Corriente estelar
    "Symbiotic*": "Very Rare",  # Estrella simbiótica
    "Unknown": "Legendary",  # Objeto de naturaleza desconocida
    "Void": "Cosmic",  # Región subdensa del universo
    "WD*": "Uncommon",  # Enana blanca
    "YellowSG*": "Uncommon",  # Supergigante amarilla
}

def classify_object(otype):
    return object_types.get(otype)

# Función para serializar los resultados
def serialize_result(result):
    return {
        "name": str(result["MAIN_ID"]),
        "ra": str(result["RA"]),
        "dec": str(result["DEC"]),
        "flux(V)": str(result["FLUX_V"]) if "FLUX_V" in result.colnames and result["FLUX_V"] is not None else None,
        "parallax": str(result["PLX_VALUE"]) if "PLX_VALUE" in result.colnames and result["PLX_VALUE"] is not None else None,
        "type": str(result["OTYPE"]),
        "category": classify_object(str(result["OTYPE"]))
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
                obj_data = serialize_result(row)
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