"""
Script para poblar automáticamente la ontología de logística
a partir de un archivo CSV utilizando la biblioteca RDFlib.

Autor: Natalia Alcázar
Asignatura: Web Semántica y Social
"""

import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

def poblar_ontologia(archivo_owl, archivo_csv, archivo_salida):
    """
    Lee un archivo CSV con datos que se envian y los inserta como individuos
    en una ontología OWL 
    
    Parámetros:
    archivo_owl (str): Ruta del archivo OWL base (vacío o con estructura)
    archivo_csv (str): Ruta del archivo CSV con los datos a insertar
    archivo_salida (str): Ruta donde se guardará la nueva ontología poblada
    """
    # 1) Cargar la ontología base
    g = Graph()
    g.parse(archivo_owl, format="xml")
    
    # 2) Definir el Namespace (El enlace base de la ontología)
    LOG = Namespace("http://www.semanticweb.org/admin/ontologies/2026/2/untitled-ontology-3#")
    g.bind("log", LOG)
    
    print("Leyendo el archivo CSV y procesando individuos...")
    
    # 3. Leer el CSV y añadir datos
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Crear las URIs (Identificadores únicos) de los individuos
            envio_uri = URIRef(LOG[row['id_envio']])
            remitente_uri = URIRef(LOG[row['remitente']])
            destinatario_uri = URIRef(LOG[row['destinatario']])
            paquete_uri = URIRef(LOG[row['paquete']])
            transportista_uri = URIRef(LOG[row['transportista']])
            vehiculo_uri = URIRef(LOG[row['vehiculo']])
            
            # Asignar a que clase pertenece cada individuo (Axiomas de clase)
            g.add((envio_uri, RDF.type, LOG.Envio))
            g.add((remitente_uri, RDF.type, LOG.Remitente))
            g.add((destinatario_uri, RDF.type, LOG.Destinatario))
            g.add((paquete_uri, RDF.type, LOG.Paquete))
            g.add((transportista_uri, RDF.type, LOG.Transportista))
            g.add((vehiculo_uri, RDF.type, LOG.Vehiculo))
            
            # Añadir Object Properties (Relaciones entre ellos)
            g.add((remitente_uri, LOG.generaEnvio, paquete_uri))
            g.add((paquete_uri, LOG.dirigidoA, destinatario_uri))
            g.add((transportista_uri, LOG.conduceVehiculo, vehiculo_uri))
            g.add((vehiculo_uri, LOG.transporta, paquete_uri))
            
            # Añadir Data Properties (Atributos como el peso)
            peso = Literal(float(row['peso']), datatype=XSD.float)
            g.add((paquete_uri, LOG.pesoKg, peso))
            
    # 4. Guardar la ontología poblada en un archivo nuevo para no pisar el original
    g.serialize(destination=archivo_salida, format="xml")
    print(f"LA ONTOLOGIA POBLADA SE HA GUARDADO COMO: {archivo_salida}")

if __name__ == "__main__":
    archivo_base = "logistica.owl" 
    archivo_datos = "datos_logistica.csv"
    archivo_final = "logistica_poblada.owl"
    
    poblar_ontologia(archivo_base, archivo_datos, archivo_final)