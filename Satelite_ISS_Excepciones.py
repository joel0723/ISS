import requests
import time
from datetime import datetime

# Tu ubicación
my_location = {
    "latitude": 18.533270,
    "longitude": -69.811722,
    "tolerance": 5  # Grados de tolerancia
}

# Función para verificar si la ISS está cerca de la ubicación del usuario
def is_iss_overhead(iss_position, my_location):
    """
    Compara la posición de la ISS con la ubicación del usuario
    para determinar si está dentro del rango de tolerancia.
    """
    lat_diff = abs(iss_position[1] - my_location["latitude"])
    lon_diff = abs(iss_position[0] - my_location["longitude"])
    return lat_diff <= my_location["tolerance"] and lon_diff <= my_location["tolerance"]

# Bucle para rastrear la posición de la ISS
while True:
    try:
        # Obtener posición actual de la ISS desde la API
        response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=5)  # Timeout para evitar bloqueos
        response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta
        
        # Convertir la respuesta a formato JSON
        data = response.json()
        
        # Extraer longitud y latitud
        iss_longitude = float(data["iss_position"]["longitude"])
        iss_latitude = float(data["iss_position"]["latitude"])
        iss_position = (iss_longitude, iss_latitude)

        # Imprimir la posición y tiempo actual
        print(f"Hora: {datetime.now()} - ISS Position: {iss_position}")

        # Verificar si la ISS está cerca del usuario
        if is_iss_overhead(iss_position, my_location):
            print("🚨 La ISS está cerca de tu ubicación!")
            break  # Salir del bucle si la ISS está cerca
        
        print("Sorry, la ISS no está ni cerca de tu ubicación!")    
    
    except requests.exceptions.Timeout:
        print("⏳ Error: La solicitud a la API ha tardado demasiado en responder. Reintentando...")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud a la API: {e}")

    except ValueError:
        print("⚠️ Error al procesar los datos de la API. Puede haber un problema con la respuesta recibida.")

    except Exception as e:
        print(f"🔴 Error inesperado: {e}")

    # Esperar 10 segundos antes de la próxima solicitud
    time.sleep(10)
