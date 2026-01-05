import unittest
import sys
import os

# Configuración del path para encontrar lavadero.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lavadero import Lavadero

class TestLavadero(unittest.TestCase):
    
    def setUp(self):
        """Prepara una nueva instancia de Lavadero antes de cada prueba."""
        self.lavadero = Lavadero()

    # --- TEST DE UTILIDAD ---
    def test_reseteo_estado_con_terminar(self):
        """Verifica que terminar() resetea todas las flags y el estado."""
        self.lavadero._hacer_lavado(True, True, True)
        self.lavadero.avanzarFase() # Para que cobre algo
        self.lavadero.terminar()
        
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertTrue(self.lavadero.ingresos > 0)

    # --- TEST 1 ---
    def test1_estado_inicial_correcto(self):
        """Test 1: Verifica el estado inicial inactivo y vacío."""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertEqual(self.lavadero.ingresos, 0.0)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertFalse(self.lavadero.secado_a_mano)
        self.assertFalse(self.lavadero.encerado)
   
    # --- TEST 2 ---
    def test2_excepcion_encerado_sin_secado(self):
        """Test 2: Encerar sin secado a mano debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.lavadero._hacer_lavado(False, False, True)

    # --- TEST 3 ---
    def test3_excepcion_lavadero_ocupado(self):
        """Test 3: No se puede iniciar lavado si ya hay uno en marcha."""
        self.lavadero._hacer_lavado(False, False, False)
        with self.assertRaises(ValueError):
            self.lavadero._hacer_lavado(False, False, False)

    # --- TESTS DE INGRESOS (4 al 8) ---
    # Nota: Usamos argumentos posicionales para evitar errores de nombre 
    # y llamamos a avanzarFase() para activar el cobro.

    def test4_ingresos_prelavado(self):
        """Test 4: Prelavado a mano = 6,50€"""
        self.lavadero._hacer_lavado(True, False, False)
        self.lavadero.avanzarFase() # Pasa a FASE_COBRANDO y suma el dinero
        self.assertEqual(self.lavadero.ingresos, 6.50)

    def test5_ingresos_secado(self):
        """Test 5: Secado a mano = 6,00€"""
        self.lavadero._hacer_lavado(False, True, False)
        self.lavadero.avanzarFase()
        self.assertEqual(self.lavadero.ingresos, 6.00)

    def test6_ingresos_secado_encerado(self):
        """Test 6: Secado y encerado = 7,20€"""
        self.lavadero._hacer_lavado(False, True, True)
        self.lavadero.avanzarFase()
        self.assertEqual(self.lavadero.ingresos, 7.20)

    def test7_ingresos_prelavado_secado(self):
        """Test 7: Prelavado y secado = 7,50€"""
        self.lavadero._hacer_lavado(True, True, False)
        self.lavadero.avanzarFase()
        self.assertEqual(self.lavadero.ingresos, 7.50)

    def test8_ingresos_todos_extras(self):
        """Test 8: Todo incluido = 8,70€"""
        self.lavadero._hacer_lavado(True, True, True)
        self.lavadero.avanzarFase()
        self.assertEqual(self.lavadero.ingresos, 8.70)

    # --- TESTS DE FLUJO DE FASES (9 al 14) ---

    def test9_flujo_sin_extras(self):
        """Test 9: Flujo rápido sin extras."""
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, False, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    def test10_flujo_prelavado(self):
        """Test 10: Flujo con prelavado."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, False, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    def test11_flujo_secado(self):
        """Test 11: Flujo con secado a mano."""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, True, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    def test12_flujo_secado_encerado(self):
        """Test 12: Flujo con secado y encerado."""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, True, True)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    def test13_flujo_prelavado_secado(self):
        """Test 13: Flujo con prelavado y secado."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, True, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    def test14_flujo_completo(self):
        """Test 14: Flujo completo con todos los extras."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, True, True)
        self.assertEqual(fases_obtenidas, fases_esperadas)

if __name__ == '__main__':
    unittest.main()