import requests
import time
from datetime import datetime

# Tu ubicación
my_location = {
    "latitude": 18.533270,
    "longitude": -69.811722,
    "tolerance": 5  # Grados de tolerancia
}

# Función para verificar si la ISS está cerca
def is_iss_overhead(iss_position, my_location):
    lat_diff = abs(iss_position[1] - my_location["latitude"])
    lon_diff = abs(iss_position[0] - my_location["longitude"])
    return lat_diff <= my_location["tolerance"] and lon_diff <= my_location["tolerance"]

# Bucle para rastrear la posición de la ISS
while True:
    # Obtener posición actual de la ISS
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # Extraer longitud y latitud
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)

    # Imprimir la posición y tiempo actual
    print(f"Hora: {datetime.now()} - ISS Position: {iss_position}")

    # Verificar si la ISS está cerca
    if is_iss_overhead(iss_position, my_location):
        print("🚨 La ISS está cerca de tu ubicación!")
        break  # Salir del bucle si la ISS está cerca
    print("Sorry, la ISS no está ni cerca de tu ubicación!")    
    # Esperar 10 segundos antes de la próxima solicitud
    time.sleep(10)
