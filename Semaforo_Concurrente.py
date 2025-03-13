import threading
import time
import random

# Estructura de la petición
class Peticion:
    def __init__(self, pedido):
        self.pedido = pedido
        self.next = None

# Variables globales
peticiones = None
consume_peticion = threading.Semaphore(0)
mutex = threading.Lock()
contador_pedido = 0
MAX_LIST_SIZE = 5  # Tamaño máximo de la lista
GET_DELAY = 1  # Tiempo de espera de la hebra consumidora
PROCESS_DELAY = 2  # Tiempo de proceso de la hebra productora

# Función de la hebra productora
def hebra_productora():
    global peticiones

    while True:
        time.sleep(random.uniform(0, PROCESS_DELAY))

        # Añadir nueva petición
        peticion = Peticion(contador_pedido)
        contador_pedido += 1

        with mutex:
            peticion.next = peticiones
            peticiones = peticion

        print(f"Hebra productora: Nuevo elemento {peticion.pedido} añadido a la lista.")
        consume_peticion.release()

# Función de la hebra consumidora
def hebra_consumidora():
    global peticiones

    while True:
        consume_peticion.acquire()

        with mutex:
            if peticiones is not None:
                elemento = peticiones.pedido
                peticiones = peticiones.next
                print(f"Hebra consumidora: Elemento {elemento} consumido de la lista.")

# Hebra principal
if __name__ == "__main__":
    # Crear hebras productora y consumidora
    hebra_prod = threading.Thread(target=hebra_productora)
    hebra_cons = threading.Thread(target=hebra_consumidora)

    # Iniciar hebras
    hebra_prod.start()
    hebra_cons.start()

    # Esperar a que ambas hebras finalicen (esto no ocurrirá en este ejemplo infinito)
    hebra_prod.join()
    hebra_cons.join()