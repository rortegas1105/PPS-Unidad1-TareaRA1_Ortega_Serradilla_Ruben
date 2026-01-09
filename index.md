# UT01.- Prueba de aplicaciones web y para dispositivos móviles

---

## Índice de contenidos

1. [Documentación y prueba del programa](#1-documentación-y-prueba-del-programa)  
   - [Apartado 1. Código comentado](#apartado-1-añade-los-comentarios-al-código-de-la-aplicación-indicando-para-qué-sirven-las-diferentes-sentencias-funciones-etc)  
   - [Apartado 2. Ejecución y depuración del programa](#apartado-2-ejecutar-el-programa-mediante-las-opciones-de-ejecución-y-depuración-del-ide)
2. [Realización de los test unitarios](#3-realización-de-los-test-unitarios-de-la-aplicación)  
   - [Apartado 3. Ejecución de los tests](#apartado-3-ejecuta-los-tests)
3. [Ejecución en entorno controlado (Sandbox)](#4-ejecución-de-la-aplicación-en-un-entorno-controlado)  
   - [Apartado 4. Ejecución en entorno Sandbox](#apartado-4-ejecución-en-entorno-sandbox)
4. [Reflexión sobre la seguridad de los lenguajes](#5-reflexión-sobre-la-infraestructura-de-seguridad-de-los-lenguajes)  
   - [Apartado 5. Reflexión personal](#apartado-5-reflexión-personal)

---

## 1. Documentación y prueba del programa

### Apartado 1. Añade los comentarios al código de la aplicación indicando para qué sirven las diferentes sentencias, funciones, etc.

A continuación podemos ver en capturas de pantalla el **código comentado**.

Estas primeras imágenes corresponden a **`lavadero.py`**:

<img width="656" height="560" alt="lavadero-1" src="capturas-pantallas/codigo1.png" />
<img width="656" height="560" alt="lavadero-2" src="capturas-pantallas/codigo2.png" />
<img width="656" height="560" alt="lavadero-3" src="capturas-pantallas/codigo3.png" />
<img width="656" height="560" alt="lavadero-4" src="capturas-pantallas/codigo4.png" />
<img width="656" height="560" alt="lavadero-5" src="capturas-pantallas/codigo5.png" />
<img width="656" height="560" alt="lavadero-6" src="capturas-pantallas/codigo6.png" />

Las siguientes imágenes corresponden a **`main_app.py`**:

<img width="656" height="560" alt="main_app-1" src="capturas-pantallas/codigo7-main.png" />
<img width="656" height="560" alt="main_app-2" src="capturas-pantallas/codigo8-main.png" />

---

## 2. Ejecución y depuración del programa

### Apartado 2. Ejecutar el programa mediante las opciones de Ejecución y Depuración del IDE.

El código tenía una serie de errores que he solucionado.  
A continuación se detallan los **errores encontrados** y sus **soluciones**:

---

### Error 1: Tipo de excepción incorrecto
**Archivo:** `lavadero.py` → método `_hacer_lavado`  
**Descripción:** Se lanzaba `RuntimeError` cuando el lavadero estaba ocupado, pero según los tests debía ser `ValueError`.  
**Solución:** Cambiar a `raise ValueError(...)`.

<img width="656" height="560" src="capturas-pantallas/error1.png" />

---

### Error 2: Precios invertidos en el método `_cobrar`
**Archivo:** `lavadero.py`  
**Descripción:** Los incrementos de precio de secado manual (+1.20 €) y encerado (+1.00 €) estaban intercambiados.  
**Solución:** Invertir los valores para que **secado = +1.00 €** y **encerado = +1.20 €**.

<img width="656" height="560" src="capturas-pantallas/error2.png" />

---

### Error 3: Lógica invertida en transición de fases
**Archivo:** `lavadero.py` → método `avanzarFase`  
**Descripción:** La condición para decidir entre secado automático y manual estaba invertida.  
**Solución:** Corregir la condición.

<img width="656" height="560" src="capturas-pantallas/error3y4.png" />

---

### Error 4: Falta de transición a fase de encerado
**Archivo:** `lavadero.py` → método `avanzarFase`  
**Descripción:** Después del secado manual no se verificaba si debía pasar a encerado.  
**Solución:** Añadir comprobación de `if self.__encerado:` para pasar a `FASE_ENCERADO`.

<img width="656" height="560" src="capturas-pantallas/error3y4.png" />

---

### Error 5: Método público vs. privado inconsistente
**Archivos:** `lavadero.py` y `main_app.py`  
**Descripción:** Los tests usaban `_hacer_lavado` pero el programa principal llamaba a `hacerLavado`.  
**Solución:** Mantener `_hacer_lavado` como interno y modificar el código principal para usarlo.

<img width="656" height="560" src="capturas-pantallas/error5.png" />

---

### Error 6: Parámetro faltante en la función
**Archivo:** `main_app.py`  
**Descripción:** Faltaba el parámetro `encerado` en una llamada a `ejecutarSimulacion`.  
**Solución:** Añadir `encerado=False`.

<img width="656" height="560" src="capturas-pantallas/error6.png" />

---

### Ejecución correcta tras las correcciones

<img width="656" height="560" src="capturas-pantallas/ejecutarPrograma.png" />

---

## 3. Realización de los test unitarios de la aplicación

### Apartado 3: Ejecuta los tests

A continuación se muestran capturas de los **tests unitarios** realizados con `unittest`.

<img width="656" height="560" src="capturas-pantallas/tests1.png" />
<img width="656" height="560" src="capturas-pantallas/tests2.png" />
<img width="656" height="560" src="capturas-pantallas/tests3.png" />

> Los errores encontrados están explicados en el [Apartado 2](#apartado-2-ejecutar-el-programa-mediante-las-opciones-de-ejecución-y-depuración-del-ide).

Tras aplicar las correcciones, todos los tests se ejecutaron correctamente:

<img width="656" height="560" src="capturas-pantallas/testsCorrectos.png" />

---

## 4. Ejecución de la aplicación en un entorno controlado

### Apartado 4: Ejecución en entorno Sandbox

Aunque el **Windows Sandbox** era mi primera opción, presentó problemas de configuración, por lo que utilicé **Sandboxie-Plus** para aislar la ejecución del programa.

<img width="656" height="560" src="capturas-pantallas/sandboxie.png" />

---

## 5. Reflexión sobre la infraestructura de seguridad de los lenguajes

### Apartado 5: Reflexión personal

Después de leer sobre las medidas de seguridad de distintos lenguajes, me he dado cuenta de que cada uno protege el código de forma diferente.  
**Python**, por ejemplo, es bastante seguro en el día a día porque gestiona la memoria de forma automática y evita muchos errores típicos. Aun así, su seguridad depende mucho del entorno donde se ejecute, ya que no tiene un sistema propio que verifique el código, así que es mejor usarlo dentro de entornos virtuales o **sandbox** para evitar problemas.

**Java** es, sin duda, uno de los más completos en cuanto a seguridad. Su máquina virtual revisa el código antes de ejecutarlo, permite firmar archivos para comprobar su origen y tiene varias librerías que ayudan a mantener las comunicaciones seguras.  
El entorno **.NET** sigue un enfoque parecido, controlando los permisos y la seguridad desde su propia máquina virtual.

En cambio, **PHP** depende más del servidor donde se ejecuta. Si no se configura bien, puede ser más vulnerable, aunque con buenas prácticas también puede ser estable.

En resumen, para mí **Java y Python** son los más equilibrados: Java por su sistema de seguridad tan completo, y Python por ser sencillo y fiable si se usa correctamente.  
Al final, la seguridad no solo depende del lenguaje, sino también de cómo se programe y del entorno donde se ejecute.

---
