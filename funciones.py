# === PROYECTO FINAL - JUEGO DEL AHORCADO EN PYGAME ===
# Instrucciones:
# - Usar funciones, listas, diccionarios y archivos.
# - No usar clases ni programación orientada a objetos.
# - El juego debe leer palabras desde un archivo de texto externo (palabras.txt).
# - Mostrar la palabra oculta en pantalla, los intentos y las letras ingresadas.
# - Dibujar el muñeco del ahorcado a medida que se cometen errores (cabeza, cuerpo, brazos, piernas).
# - Mostrar mensaje final al ganar o perder.
# - Organizar el código con funciones bien nombradas.
# - El código debe estar comentado línea por línea.
# - Solo las partes del cuerpo deben contar como errores, no el soporte del ahorcado.

import pygame
import random 
import sys 

# No necesitamos importar interfaz ni personaje aquí si sus funciones no se usan directamente en este módulo.
# pygame.init() # Se inicializa en main.py

# ----------------- CARGAR UNA IMAGEN -----------------
def cargar_imagen(r_imagen:str, x:int, y:int):
    """
        Carga y escala una imagen desde la ruta especificada.

    Args:
        n_imagen (str): La ruta del archivo de imagen.
        x (int): El ancho deseado para la imagen escalada.
        y (int): El alto deseado para la imagen escalada.

    """
    escalar = None 
    try:
        imagen = pygame.image.load(r_imagen) 
        escalar = pygame.transform.scale(imagen, (x,y)) 

        return escalar #Devuelve la imagen escalada
    except Exception as e: 
        print("Error al cargar la imagen: " , e) 
        return None 
    


def cargar_sonido(r_sonido:str):

    """
        Carga el sonido desde un archivo

        Arg:
            r_sonido (int): Espera la ruta de sonido

    """

    try:
        sonido = pygame.mixer.Sound(r_sonido)
        
        return sonido
    except Exception as e: 
        print("Error al cargar el sonido: ", e) 
        return None 
    
    




# ----------------- CARGAR PALABRAS DESDE ARCHIVO -----------------
def cargar_palabras(lista_palabras:list):
    """
    Carga una lista de palabras desde un archivo de texto.

    Args:
        lista_palabras (list): La lista a la que se añadirán las palabras.
    """
    try:
        with open('palabras.txt', 'r', encoding='utf-8') as archivo: #Utilizo with open para abrir el txt y "r" para leerlo
            for palabra in archivo: # Por cada palabra que tiene el txt
                palabra = palabra.rstrip("\n") # Elimino el salto de linea para que no se incluya en la lista
                lista_palabras.append(palabra) # Agrego la palabra a la lista
    
        return lista_palabras #Devuelvo la lista de palabras llena
    except Exception as e: 
        print("Error al cargar palabras desde el .txt: ", e) 
        sys.exit() # Salir en caso error
    





# ----------------- ELEGIR PALABRA AL AZAR -----------------
def elegir_palabra(lista_palabras:list):
    """
        Elije una palabra al azar desde una lista de palabras y devuelve la lista con la palabra separada por letras

        Arg:
            lista_palabras:list → Espera una lista con str

    """
    
    palabra_al_azar = [] #Creo lista vacia donde guardaré la palabra
    palabra_al_azar_x_letras = [] #Creo la lista vacia donde guardaré la palabra por letras

    # Elegir una palabra aleatoria de la lista y convertirla a mayúsculas
    indice_azar = random.randint(0,len(lista_palabras) - 1) #Elijo un indice al azar entre 0 y el largo de la lista - 1
    palabra_al_azar = lista_palabras[indice_azar].upper() #Guardo la palabra completa y la paso a mayusculas
    palabra_al_azar_x_letras += lista_palabras[indice_azar].upper() #Guardo la palabra con cada letra por separado en la lista y lo paso a mayusculas

    return palabra_al_azar_x_letras , palabra_al_azar #Devuelvo la lista de palabras completa y la lista por letras

# ----------------- VERIFICAR LETRA -----------------
def verificar_letra(letra_ingresada,palabra_secreta_x_letras,letras_adivinadas,letras_intentadas,errores):
    
    """
    Recibe el ingreso del usuario, la palabra a adivinar, la lista con las palabras ya ingresadas por el usuario, las 
    que corresponden a la palabra a adivinar y la cantidad de errores que ya cometió el usuario

    Busca el ingreso actual en una lista donde se guardan los intentos del usuario, si no está, lo agrega a los intentos.
    Si no pertenece a la palabra a adivinar, aumenta la cant de errores, si pertenece, se agrega a las letras adivinadas.   
    """
    sonido_error = cargar_sonido("error.wav")

    # Si la letra no ha sido intentada antes
    if letra_ingresada not in letras_intentadas:
        letras_intentadas.append(letra_ingresada) # Agrega la letra a las letras intentadas

        # Si la letra NO está en la palabra secreta
        if letra_ingresada not in palabra_secreta_x_letras:
            errores += 1 # Incrementa el contador de errores
            sonido_error.play() # Reproduce el sonido de error
        else:
            # Si la letra está en la palabra, la agrega a las letras adivinadas
            letras_adivinadas.append(letra_ingresada)
  
    return errores #Devuelvo la cantidad de errores



