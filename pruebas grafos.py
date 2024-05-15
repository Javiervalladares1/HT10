import unittest
import os
from tarea5 import Grafo

class TestGrafo(unittest.TestCase):
    def setUp(self):
        # Crear un archivo temporal de prueba
        self.test_file = 'test_logistica.txt'
        with open(self.test_file, 'w') as f:
            f.write('Paris, London, 5, 6, 7, 8\n')
            f.write('Paris, Berlin, 2, 3, 4, 5\n')
            f.write('London, Berlin, 3, 4, 5, 6\n')
            f.write('London, Rome, 1, 2, 3, 4\n')
            f.write('Berlin, Rome, 4, 5, 6, 7\n')

    def test_leer_archivo(self):
        grafo = Grafo()
        grafo.leer_archivo(self.test_file)
        self.assertEqual(len(grafo.ciudades), 4)
        self.assertEqual(len(grafo.matriz_adyacencia), 10)

    def test_escribir_archivo(self):
        grafo = Grafo()
        grafo.leer_archivo(self.test_file)
        grafo.escribir_archivo()
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 5)  # El archivo debe tener 5 líneas

    def test_floyd_warshall(self):
        grafo = Grafo()
        grafo.leer_archivo(self.test_file)
        dist, _ = grafo.floyd_warshall(0)  # Probamos con clima normal
        self.assertEqual(dist[0][3], 6)  # Distancia entre Paris y Rome

   

    def test_centro_grafo(self):
        grafo = Grafo()
        grafo.leer_archivo(self.test_file)
        centro = grafo.centro_grafo(0)  # Clima normal
        self.assertEqual(centro, 'Berlin')

    def test_modificar_grafo(self):
        grafo = Grafo()
        grafo.leer_archivo(self.test_file)
        grafo.modificar_grafo('conexion', 'Paris', 'Rome', [10, 12, 15, 20])  # Nueva conexión
        distancia, _ = grafo.camino_mas_corto('Paris', 'Rome', 0)  # Clima normal
        self.assertEqual(distancia, 6)

    def tearDown(self):
        # Eliminar el archivo temporal de prueba
        os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
