import sys

class Grafo:
    def __init__(self):
        self.ciudades = {}
        self.matriz_adyacencia = {}
        self.ciudades_idx = {}

    def leer_archivo(self, filename):
        self.filename = filename  # Guardar el nombre del archivo para futuras escrituras
        with open(filename, 'r') as f:
            lineas = f.readlines()

        for linea in lineas:
            datos = linea.strip().split(',')
            if len(datos) != 6:
                print(f"Error en el formato de la línea: {linea}")
                continue

            ciudad1, ciudad2 = datos[0].strip(), datos[1].strip()
            try:
                tiempos = list(map(int, datos[2:]))
            except ValueError:
                print(f"Error en la conversión de tiempos para la línea: {linea}")
                continue

            if ciudad1 not in self.ciudades:
                self.ciudades[ciudad1] = len(self.ciudades)
                self.ciudades_idx[self.ciudades[ciudad1]] = ciudad1

            if ciudad2 not in self.ciudades:
                self.ciudades[ciudad2] = len(self.ciudades)
                self.ciudades_idx[self.ciudades[ciudad2]] = ciudad2

            self.matriz_adyacencia[(ciudad1, ciudad2)] = tiempos
            self.matriz_adyacencia[(ciudad2, ciudad1)] = tiempos

    def escribir_archivo(self):
        with open(self.filename, 'w') as f:
            for (ciudad1, ciudad2), tiempos in self.matriz_adyacencia.items():
                if ciudad1 < ciudad2:  # Para evitar duplicados, escribir solo una dirección
                    f.write(f"{ciudad1}, {ciudad2}, {tiempos[0]}, {tiempos[1]}, {tiempos[2]}, {tiempos[3]}\n")

    def floyd_warshall(self, clima_idx):
        n = len(self.ciudades)
        dist = [[sys.maxsize] * n for _ in range(n)]
        next_node = [[-1] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for (ciudad1, ciudad2), tiempos in self.matriz_adyacencia.items():
            i, j = self.ciudades[ciudad1], self.ciudades[ciudad2]
            dist[i][j] = tiempos[clima_idx]
            dist[j][i] = tiempos[clima_idx]
            next_node[i][j] = j
            next_node[j][i] = i

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        return dist, next_node

    def camino_mas_corto(self, origen, destino, clima_idx):
        dist, next_node = self.floyd_warshall(clima_idx)
        i, j = self.ciudades[origen], self.ciudades[destino]

        if dist[i][j] == sys.maxsize:
            return None, None

        path = [origen]
        while i != j:
            i = next_node[i][j]
            path.append(self.ciudades_idx[i])
        return dist[self.ciudades[origen]][self.ciudades[destino]], path

    def centro_grafo(self, clima_idx):
        dist, _ = self.floyd_warshall(clima_idx)
        max_dist = [max(row) for row in dist]
        min_max_dist = min(max_dist)
        centro_idx = max_dist.index(min_max_dist)
        return self.ciudades_idx[centro_idx]

    def modificar_grafo(self, tipo_modificacion, ciudad1, ciudad2=None, tiempos=None):
        if tipo_modificacion == 'interrupcion':
            if (ciudad1, ciudad2) in self.matriz_adyacencia:
                del self.matriz_adyacencia[(ciudad1, ciudad2)]
                del self.matriz_adyacencia[(ciudad2, ciudad1)]
        elif tipo_modificacion == 'conexion':
            self.matriz_adyacencia[(ciudad1, ciudad2)] = tiempos
            self.matriz_adyacencia[(ciudad2, ciudad1)] = tiempos
        elif tipo_modificacion == 'clima':
            if (ciudad1, ciudad2) in self.matriz_adyacencia:
                self.matriz_adyacencia[(ciudad1, ciudad2)][tiempos[0]] = tiempos[1]
                self.matriz_adyacencia[(ciudad2, ciudad1)][tiempos[0]] = tiempos[1]
        self.escribir_archivo()  # Escribir los cambios en el archivo después de cada modificación

def main():
    grafo = Grafo()
    grafo.leer_archivo('logistica.txt')

    while True:
        print("\nOpciones:")
        print("1. Consultar la ruta más corta")
        print("2. Determinar el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Finalizar")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            origen = input("Ingrese la ciudad origen: ")
            destino = input("Ingrese la ciudad destino: ")
            clima = input("Ingrese el clima (normal, lluvia, nieve, tormenta): ")
            clima_idx = {'normal': 0, 'lluvia': 1, 'nieve': 2, 'tormenta': 3}[clima]
            distancia, camino = grafo.camino_mas_corto(origen, destino, clima_idx)
            if distancia is None:
                print("No hay ruta disponible entre las ciudades.")
            else:
                print(f"Distancia: {distancia} horas")
                print("Ruta:", " -> ".join(camino))
        elif opcion == 2:
            clima = input("Ingrese el clima (normal, lluvia, nieve, tormenta): ")
            clima_idx = {'normal': 0, 'lluvia': 1, 'nieve': 2, 'tormenta': 3}[clima]
            centro = grafo.centro_grafo(clima_idx)
            print(f"El centro del grafo es: {centro}")
        elif opcion == 3:
            tipo_modificacion = input("Ingrese el tipo de modificación (interrupcion, conexion, clima): ")
            ciudad1 = input("Ingrese la primera ciudad: ")
            if tipo_modificacion == 'conexion' or tipo_modificacion == 'clima':
                ciudad2 = input("Ingrese la segunda ciudad: ")
                if tipo_modificacion == 'conexion':
                    tiempos = list(map(int, input("Ingrese los tiempos (normal lluvia nieve tormenta): ").split()))
                    grafo.modificar_grafo(tipo_modificacion, ciudad1, ciudad2, tiempos)
                elif tipo_modificacion == 'clima':
                    clima = input("Ingrese el clima (normal, lluvia, nieve, tormenta): ")
                    tiempo = int(input("Ingrese el nuevo tiempo: "))
                    clima_idx = {'normal': 0, 'lluvia': 1, 'nieve': 2, 'tormenta': 3}[clima]
                    grafo.modificar_grafo(tipo_modificacion, ciudad1, ciudad2, (clima_idx, tiempo))
            elif tipo_modificacion == 'interrupcion':
                ciudad2 = input("Ingrese la segunda ciudad: ")
                grafo.modificar_grafo(tipo_modificacion, ciudad1, ciudad2)
        elif opcion == 4:
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
