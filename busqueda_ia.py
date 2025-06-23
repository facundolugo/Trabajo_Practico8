import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

#Preparamos los documentos para la busqueda

def preparar_texto(texto):
    texto = texto.lower() # Todo a minusculas
    # Quita cualquier cosa que NO sea una letra (a-z) o un espacio.
    texto = re.sub(r'[^a-z\s]', ' ', texto) # Quita cosas raras 
    palabras = word_tokenize(texto) # Divide el texto en palabras
    palabras_irrelevantes = set(stopwords.words())   
    palabras_limpias = []
    
    for palabra in palabras:
        if palabra and palabra not in palabras_irrelevantes:
            palabras_limpias.append(palabra)
    return palabras_limpias

def crear_indice_documentos(todos_los_documentos):
    #Hace un 'indice' que nos dice en que documentos aparece cada palabra.
    indice = {}
    for id_documento, texto_documento in todos_los_documentos.items():
        palabras_del_doc = preparar_texto(texto_documento)
        for palabra in palabras_del_doc:
            if palabra not in indice:
                indice[palabra] = set()
            indice[palabra].add(id_documento)
    return indice

#Como buscamos en los documentos

def buscar_en_indice(consulta_del_usuario, indice):
    #Busca documentos usando la consulta (con AND, OR, NOT).
    def limpiar_palabra_consulta(palabra):
        palabra = palabra.lower() # A minusculas
        palabra = re.sub(r'[^a-z\s]', '', palabra) # Quita cosas raras
        return palabra.strip() # Quita espacios extra
    
    consulta_en_minusculas = consulta_del_usuario.lower() 

    if ' and ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' and ')
        p1 = limpiar_palabra_consulta(partes[0])
        p2 = limpiar_palabra_consulta(partes[1])
        return indice.get(p1, set()).intersection(indice.get(p2, set()))
        
    elif ' or ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' or ')
        p1 = limpiar_palabra_consulta(partes[0])
        p2 = limpiar_palabra_consulta(partes[1])
        return indice.get(p1, set()).union(indice.get(p2, set()))
        
    elif ' not ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' not ')
        p_positiva = limpiar_palabra_consulta(partes[0])
        p_negativa = limpiar_palabra_consulta(partes[1])
        return indice.get(p_positiva, set()) - indice.get(p_negativa, set())
        
    else:
        palabra_unica = limpiar_palabra_consulta(consulta_del_usuario)
        return indice.get(palabra_unica, set())

documentos_ia_ejemplo = {
    "doc1": "La inteligencia artificial esta revolucionando la tecnologia.",
    "doc2": "El aprendizaje automatico es clave en la inteligencia artificial.",
    "doc3": "Procesamiento del lenguaje natural y redes neuronales.",
    "doc4": "Las redes neuronales son fundamentales en deep learning.",
    "doc5": "El futuro de la IA esta en el aprendizaje profundo."
}

print("Buscador de Documentos: Inteligencia Artificial")
indice_ia = crear_indice_documentos(documentos_ia_ejemplo)

while True:
    pregunta = input("Escribir busqueda (ej: inteligencia AND artificial, o 'salir'): ")
    if pregunta.lower() == 'salir':
        break
    
    resultados_encontrados = buscar_en_indice(pregunta, indice_ia)
    print(f" Documentos encontrados: {resultados_encontrados}\n")
