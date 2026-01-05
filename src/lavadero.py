# lavadero.py

class Lavadero:
    """
    Simula el estado y las operaciones de un túnel de lavado de coches.
    Cumple con los requisitos de estado, avance de fase y reglas de negocio.
    """
    # Constantes que representan cada fase del proceso del tunel de lavado
    
    FASE_INACTIVO = 0
    FASE_COBRANDO = 1
    FASE_PRELAVADO_MANO = 2
    FASE_ECHANDO_AGUA = 3
    FASE_ENJABONANDO = 4
    FASE_RODILLOS = 5
    FASE_SECADO_AUTOMATICO = 6
    FASE_SECADO_MANO = 7
    FASE_ENCERADO = 8

    def __init__(self):
        """
        Constructor de la clase. Inicializa el lavadero.
        Cumple con el requisito 1.
        """
        self.__ingresos = 0.0
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False
        self.terminar() # Asegura que todos los estados esten en valores iniciales

    # Propiedades para acceder a los atributos privados de forma controlada

    @property
    def fase(self):
        """Devuelve la fase actual del lavado"""
        return self.__fase

    @property
    def ingresos(self):
        """Devuelve los ingresos acumulados"""
        return self.__ingresos

    @property
    def ocupado(self):
        """Indica si el lavadero esta ocupado"""
        return self.__ocupado
    
    @property
    def prelavado_a_mano(self):
        """Indica si el lavado actual tiene prelavado a mano."""
        return self.__prelavado_a_mano

    @property
    def secado_a_mano(self):
        """Indica si el lavado actual incluye secado manual"""
        return self.__secado_a_mano

    @property
    def encerado(self):
        """Indica si el lavado actual incluye encerado."""
        return self.__encerado


    # METODOS


    def terminar(self):
        """Restaura el estado del lavadero a inactivo."""
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False

    # ERROR CORREGIDO  : Se cambio el nombre de hacerLavado a _hacer_lavado para coincidir 
    # con los tests unitarios

    def _hacer_lavado(self, prelavado_a_mano, secado_a_mano, encerado):
        """
        Inicia un nuevo ciclo de lavado, validando reglas de negocio.

        :param prelavado_a_mano: Booleano que indica si se solicita prelavado a mano
        :param secado_a_mano: Booleano que indica si se solicita secado a mano
        :param encerado: Booleano que indica si se solicita encerado
        
        :raises RuntimeError: Si el lavadero está ocupado (Requisito 3).
        :raises ValueError: Si se intenta encerar sin secado a mano (Requisito 2).
        """
        # ERROR CORREGIDO : La excepción original era RuntimeError, pero según  los tests debe ser ValueError 
        if self.__ocupado:
            raise ValueError("No se puede iniciar un nuevo lavado mientras el lavadero está ocupado")
        
        # Validación Requisito: Encerado requiere secado a mano.
        if not secado_a_mano and encerado:
            raise ValueError("No se puede encerar el coche sin secado a mano")
        
        self.__fase = self.FASE_INACTIVO  
        self.__ocupado = True
        self.__prelavado_a_mano = prelavado_a_mano
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado
        

    def _cobrar(self):
        """
        Calcula y añade los ingresos según las opciones seleccionadas (Requisitos 4-8).
        Precio base: 5.00€ (Implícito, 5.00€ de base + 1.50€ de prelavado + 1.00€ de secado + 1.20€ de encerado = 8.70€)
        
        """
        #ERROR CORREGIDO : Los precios estaban invertidos.
        #Original: secado = 1.20€, encerado = 1.00€
        #Corregido: secado = 1.00€, encerado = 1.20€

        coste_lavado = 5.00
        
        
        if self.__prelavado_a_mano:
            coste_lavado += 1.50 
        
         # ERROR CORREGIDO: El secado a mano añade 1.00€
        if self.__secado_a_mano:
            coste_lavado += 1.00 

        # ERROR CORREGIDO: El encerado añade 1.20€ sobre el precio con secado
        if self.__encerado:
            coste_lavado += 1.20 

        # Acumular ingresos    
        self.__ingresos += coste_lavado
        return coste_lavado
        

    def avanzarFase(self):
        """Avanza al siguiente estado del ciclo de lavado."""
       
        if not self.__ocupado:
            return

        if self.__fase == self.FASE_INACTIVO:
            # Primera transición: cobrar y pasar a fase de cobro
            coste_cobrado = self._cobrar()
            self.__fase = self.FASE_COBRANDO
            print(f" (COBRADO: {coste_cobrado:.2f} €) ", end="")

        elif self.__fase == self.FASE_COBRANDO:
            # Decidir si ir a prelavado manual o directamente a echar agua
            if self.__prelavado_a_mano:
                self.__fase = self.FASE_PRELAVADO_MANO
            else:
                self.__fase = self.FASE_ECHANDO_AGUA 
        
        elif self.__fase == self.FASE_PRELAVADO_MANO:
            self.__fase = self.FASE_ECHANDO_AGUA
        
        elif self.__fase == self.FASE_ECHANDO_AGUA:
            self.__fase = self.FASE_ENJABONANDO

        elif self.__fase == self.FASE_ENJABONANDO:
            self.__fase = self.FASE_RODILLOS
        
        elif self.__fase == self.FASE_RODILLOS:
            # ERROR CORREGIDO : La lógica estaba invertida
            # Original: si secado_a_mano -> FASE_SECADO_AUTOMATICO 
            # Corregido: si secado_a_mano -> FASE_SECADO_MANO 
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_MANO  
            else:
                self.__fase = self.FASE_SECADO_AUTOMATICO  
        
        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            # Fin del ciclo sin secado manual
            self.terminar()
        
        elif self.__fase == self.FASE_SECADO_MANO:
            # ERROR CORREGIDO : Faltaba transición a encerado
            # Después de secado manual, verificar si hay encerado
            if self.__encerado:
                self.__fase = self.FASE_ENCERADO  
            else:
                self.terminar()  # Fin del ciclo sin encerado
        
        elif self.__fase == self.FASE_ENCERADO:
            self.terminar()  # Fin del ciclo con encerado
        
        else:
            # Control de errores , fase no reconocida
            raise RuntimeError(f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar...")
   
   
   
   
    def imprimir_fase(self):
        """Muestra por consola el nombre descriptivo de la fase actual."""
        fases_map = {
            self.FASE_INACTIVO: "0 - Inactivo",
            self.FASE_COBRANDO: "1 - Cobrando",
            self.FASE_PRELAVADO_MANO: "2 - Haciendo prelavado a mano",
            self.FASE_ECHANDO_AGUA: "3 - Echándole agua",
            self.FASE_ENJABONANDO: "4 - Enjabonando",
            self.FASE_RODILLOS: "5 - Pasando rodillos",
            self.FASE_SECADO_AUTOMATICO: "6 - Haciendo secado automático",
            self.FASE_SECADO_MANO: "7 - Haciendo secado a mano",
            self.FASE_ENCERADO: "8 - Encerando a mano",
        }
        print(fases_map.get(self.__fase, f"{self.__fase} - En estado no válido"), end="")

  
    def imprimir_estado(self):
        """Muestra un resumen completo del estado actual del lavadero."""
        print("----------------------------------------")
        print(f"Ingresos Acumulados: {self.ingresos:.2f} €")
        print(f"Ocupado: {self.ocupado}")
        print(f"Prelavado a mano: {self.prelavado_a_mano}")
        print(f"Secado a mano: {self.secado_a_mano}")
        print(f"Encerado: {self.encerado}")
        print("Fase: ", end="")
        self.imprimir_fase()
        print("\n----------------------------------------")
        
    # Esta función es útil para pruebas unitarias, no es parte del lavadero real
    # nos crea un array con las fases visitadas en un ciclo completo

    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """Ejecuta un ciclo completo y devuelve la lista de fases visitadas.
        :param prelavado: Booleano para prelavado manual
        :param secado: Booleano para secado manual
        :param encerado: Booleano para encerado
        :return: Lista de fases por las que pasó el lavado
        """
        self._hacer_lavado(prelavado, secado, encerado)
        fases_visitadas = [self.fase]

        while self.ocupado:
            # Usamos un límite de pasos para evitar bucles infinitos en caso de error
            if len(fases_visitadas) > 15:
                raise Exception("Bucle infinito detectado en la simulación de fases.")
            self.avanzarFase()
            fases_visitadas.append(self.fase)

        return fases_visitadas
