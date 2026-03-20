# Práctica 4: Poblado Automático de la Ontología de Logística

Este repositorio contiene la implementación en Python para poblar automáticamente una ontología OWL del dominio de la logística, partiendo de un modelo base y utilizando datos estructurados de un archivo CSV. 

El desarrollo se ha realizado haciendo uso de la biblioteca `rdflib`

## Requisitos Previos

Para poder ejecutar este proyecto, es necesario tener instalado en el sistema:
* [Python 3](https://www.python.org/downloads/) 
* El gestor de paquetes `pip` 

## Replicación del Entorno Virtual

Para garantizar la replicabilidad del proyecto y evitar conflictos de versiones, se ha utilizado el módulo nativo `venv` para la creación de un entorno virtual, fijando las dependencias en el archivo `requirements.txt`. 

Lo que he hecho para replicar el entorno:

1. Clonar el repositorio 
```bash
git clone mi_repo
cd p4
```
2. Crear el entorno virtual 
```bash
python -m venv venv
```

3. Activar el entorno virtual
```bash
.\venv\Scripts\activate
```

4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

## Ejecución de la Aplicación
Con el entorno virtual activado y las dependencias instaladas, el sistema está listo para ejecutarse.

1. Archivos necesarios en el directorio raíz:

### logistica.owl: La ontología base con la taxonomía (clases y propiedades) ya diseñada en Protégé.

### datos_logistica.csv: El archivo de datos con los registros de envíos, clientes, transportistas, etc.

### poblar.py: El script principal de Python.

2. Ejecutar el script:
Lanzar el siguiente comando en la terminal:
```bash
python poblar.py
```



3. Resultado esperado:
El script leerá el archivo CSV, parseará la ontología base e instanciará los individuos asignándoles sus respectivas Object Properties y Data Properties.

Al finalizar, mostrará un mensaje de éxito por consola y generará un nuevo archivo llamado logistica_poblada.owl. Este archivo puede abrirse directamente en Protégé para comprobar la correcta instanciación de las clases y usar el razonador sobre los nuevos datos.

## ¿Cómo he hecho el código? (Explicación paso a paso)

El script `poblar.py` actúa como un "traductor" que convierte los datos planos de una tabla (CSV) en conocimiento semántico estructurado (Ontología OWL). A continuación, explico el flujo lógico que he diseñado para lograrlo:

**1. Preparación y carga del modelo base**
Primero, instancio un grafo vacío (`Graph()`) utilizando `rdflib` y cargo dentro mi archivo original `logistica.owl` mediante la función `parse()`. 
Después, defino el **Namespace** (el IRI o "apellido" de mi ontología). 

**2. Lectura del archivo CSV**
Utilizo la librería nativa `csv` de Python para abrir el archivo `datos_logistica.csv`. Mediante un bucle `for row in reader`, el programa lee el archivo fila por fila, permitiéndome extraer la información de cada columna (remitente, destinatario, paquete, etc.).

**3. Creación de Individuos (URIs)**
En la Web Semántica, un individuo no es solo un texto, es un recurso único. Por ello, cojo el texto de cada celda del CSV (por ejemplo, "Paco_Repartidor") y lo combino con el Namespace usando `URIRef()`. Así, transformo un simple nombre en un identificador web único y válido.

**4. Inyección de conocimiento**
Una vez tengo los individuos creados en la memoria de Python, empiezo a añadir la lógica a la ontología (Sujeto -> Predicado -> Objeto) a través de la función `g.add()`:

* **Asignación de Clases:** Uso la propiedad estándar `RDF.type` para decirle al programa a qué clase pertenece cada individuo (ej. *Paco_Repartidor es de tipo Transportista*).
* **Object Properties:** Conecto los individuos entre sí utilizando las propiedades que creé en Protégé (ej. *Transportista -> conduceVehiculo -> Vehiculo*).
* **Data Properties:** Para los atributos numéricos o de texto, como el peso del paquete, utilizo la función `Literal()`. Además, me aseguro de convertir el texto del CSV a número (`float`) y lo etiqueto semánticamente con `XSD.float` para que el razonador entienda que es un valor decimal matemático y no una simple palabra.

**5. Guardado del nuevo modelo**
Una vez que el bucle ha terminado de procesar todas las filas del CSV y el grafo está lleno de conocimiento nuevo, utilizo la función `serialize()` para exportar todo el conjunto a un archivo nuevo (`logistica_poblada.owl`). Así, protejo el archivo original por si necesito volver a ejecutar el proceso.
