# tests/test_lavadero_unittest.py

import unittest
# Importamos la clase Lavadero desde el módulo padre
from lavadero import Lavadero

class TestLavadero(unittest.TestCase):
    
    # Método que se ejecuta antes de cada test.
    # Es el equivalente del @pytest.fixture en este contexto.
    def setUp(self):
        """Prepara una nueva instancia de Lavadero antes de cada prueba."""
        self.lavadero = Lavadero()

    
        
    # ----------------------------------------------------------------------
    # TESTS  
    # ----------------------------------------------------------------------
    

    # ----------------------------------------------------------------------    
    # Función para resetear el estado cuanto terminamos una ejecución de lavado
    # ----------------------------------------------------------------------
    def test_reseteo_estado_con_terminar(self):
        """Test 4: Verifica que terminar() resetea todas las flags y el estado."""
        self.lavadero._hacer_lavado(True, True, True)
        self.lavadero._cobrar()
        self.lavadero.terminar()
        
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertTrue(self.lavadero.ingresos > 0) # Los ingresos deben mantenerse

    # TEST 1
        
    def test1_estado_inicial_correcto(self):
        """Test 1: Verifica que el estado inicial es Inactivo y con 0 ingresos."""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertEqual(self.lavadero.ingresos, 0.0)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertFalse(self.lavadero.secado_a_mano)
        self.assertFalse(self.lavadero.encerado)
   
    # TEST 2

    def test2_excepcion_encerado_sin_secado(self):
        """Test 2: Comprueba que encerar sin secado a mano lanza ValueError."""
        # _hacer_lavado: (Prelavado: False, Secado a mano: False, Encerado: True)
        with self.assertRaises(ValueError):
            self.lavadero._hacer_lavado(False, False, True)

      # TEST 3

    def test3_excepcion_lavadero_ocupado(self):
        """Test 3: Se produce ValueError si ya hay un lavado en marcha"""
        self.lavadero._hacer_lavado(False, False, False) # Iniciamos un lavado
        with self.assertRaises(ValueError):
            self.lavadero._hacer_lavado(False, False, False)

    # TEST 4

    def test4_ingresos_prelavado(self):
        """Test 4: Lavado con prelavado a mano = 6,50€"""
        self.lavadero._hacer_lavado(prelavado=True, secado=False, encerado=False)
        self.assertEqual(self.lavadero.ingresos, 6.50)



    # TEST 5

    def test5_ingresos_secado(self):
        """Test 5: Lavado con secado a mano = 6,00€"""
        self.lavadero._hacer_lavado(prelavado=False, secado=True, encerado=False)
        self.assertEqual(self.lavadero.ingresos, 6.00)



    # TEST 6

    def test6_ingresos_secado_encerado(self):
        """Test 6: Lavado con secado y encerado = 7,20€"""
        self.lavadero._hacer_lavado(prelavado=False, secado=True, encerado=True)
        self.assertEqual(self.lavadero.ingresos, 7.20)


    # TEST 7

    def test7_ingresos_prelavado_secado(self):
        """Test 7: Lavado con prelavado y secado = 7,50€"""
        self.lavadero._hacer_lavado(prelavado=True, secado=True, encerado=False)
        self.assertEqual(self.lavadero.ingresos, 7.50)


    # TEST 8

    def test8_ingresos_todos_extras(self):
        """Test 8: Lavado con prelavado, secado y encerado = 8,70€[cite: 37, 79]."""
        self.lavadero._hacer_lavado(prelavado=True, secado=True, encerado=True)
        self.assertEqual(self.lavadero.ingresos, 8.70)




    # ----------------------------------------------------------------------
    # Tests de flujo de fases
    # Utilizamos la función def ejecutar_y_obtener_fases(self, prelavado, secado, encerado)
    # Estos tests dan errores ya que en el código original hay errores en las las fases esperados, en los saltos.
    # ----------------------------------------------------------------------

     # TEST 9

    def test9_flujo_sin_extras(self):
        """Test 9: Simula el flujo rápido sin opciones opcionales."""
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
         # Ejecutar el ciclo completo y obtener las fases
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, False, False)
         # Verificar que las fases obtenidas coinciden con las esperadas
        self.assertEqual(fases_obtenidas, fases_esperadas)

     # TEST 10

    def test10_flujo_prelavado(self):
        """Test 10: Flujo con prelavado a mano"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, False, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    # TEST 11

    def test11_flujo_secado(self):
        """Test 11: Flujo con secado a mano"""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, True, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    # TEST 12

    def test12_flujo_secado_encerado(self):
        """Test 12: Flujo con secado y encerado"""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(False, True, True)
        self.assertEqual(fases_obtenidas, fases_esperadas)


    # TEST 13

    def test13_flujo_prelavado_secado(self):
        """Test 13: Flujo con prelavado y secado"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, True, False)
        self.assertEqual(fases_obtenidas, fases_esperadas)

    # TEST 14

    def test14_flujo_completo(self):
        """Test 14: Flujo con prelavado, secado y encerado"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(True, True, True)
        self.assertEqual(fases_obtenidas, fases_esperadas)
    
 
# Bloque de ejecución para ejecutar los tests si el archivo es corrido directamente
if __name__ == '__main__':
    unittest.main()