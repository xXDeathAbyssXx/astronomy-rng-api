from hypatie.catalogues import Catalogue
import os

# Diccionario de catálogos con sus respectivos nombres y tablas
catalogues = {
    'lqac5': 'Large Quasar Astrometric Catalogue (5th release)',
    'ucac4': 'U.S. Naval Observatory CCD Astrograph Catalog (4th release)',
    'hipparcos': 'HIgh Precision PARallax COllecting Satellite (Hipparcos)',
    'sdss12': 'SDSS Photometric Catalogue, (Release 12)',
    'glimpse': 'GLIMPSE Source Catalog (I + II + 3D) (IPAC 2008)',
    'gaia2': 'Gaia data release 2',
    'gaia3': 'Gaia data release 3',
    'dfgrs2': '2dF Galaxy Redshift Survey',
    'glade2': 'GLADE v2.3 catalog (Galaxy List for the Advanced Detector Era)'
}

# Crear el directorio para guardar los archivos
output_dir = "catalogue_data2"
os.makedirs(output_dir, exist_ok=True)

# Descargar y guardar los datos de cada catálogo
for key, name in catalogues.items():
    print(f"Downloading data from {name} ({key})...")
    cat = Catalogue(key, n_max=1000000)  # 1M = 100mb
    data, meta = cat.download()

    # Guardar los datos en un archivo de texto
    output_file = os.path.join(output_dir, f"{key}.txt")
    data.to_csv(output_file, index=False)

    print(f"Data from {name} ({key}) saved to: {output_file}")
