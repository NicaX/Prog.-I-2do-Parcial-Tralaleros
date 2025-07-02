import pygame
import funciones as f

def crear_personaje():
    '''
        Crea el diccionario de un personaje con sus caracteristicas
    '''
    try:
        dicc_personaje = {} # Inicializo el diccionario del personaje
        dicc_personaje['superficie'] = f.cargar_imagen("personaje.png", 50, 50 ) #Cargo el tiburon
        dicc_personaje['rect'] = pygame.Rect(500, 350, 50, 50) # Se crea un rectangulo y se usara de colisonador
    except pygame.error as e: 
        print("Error al cargar la imagen del personaje 'personaje.png': ",)
        # En caso de error cremaos un diccionario para que no falle
        dicc_personaje = {
        'superficie': pygame.Surface((50, 50)),
        'rect': pygame.Rect(5, 5, 40, 40)
        }
        dicc_personaje['superficie'].fill((255, 0, 255))

    return dicc_personaje #Devuelvo el diccionario del personaje
        
 

def mover_personaje(personaje, ancho_pantalla, alto_pantalla, velocidad=5):
    """
        Mueve el personaje con una velocidad seteada en 5 que puede modificarse
        El personaje colisiona con los bordes de la pantalla y no puede irse fuera
        de los limites de la misma

    Args:
        personaje (dict): Espera el diccionario del personaje
        ancho_pantalla (int): El ancho de la pantalla del juego
        alto_pantalla (int): El alto de la pantalla del juego
    """
    teclas = pygame.key.get_pressed() #Guardo el modulo de las teclas presionadas en una variable

    if teclas[pygame.K_LEFT]: # Si la tecla corresponde a la flechita izquierda
        personaje["rect"].x -= velocidad # Me muevo hacia la izquierda (-x)
    if teclas[pygame.K_RIGHT]: # Si la tecla corresponde a la flechita derecha
        personaje["rect"].x += velocidad  # Me muevo hacia la izquierda (+x)
    if teclas[pygame.K_UP]:  # Si la tecla corresponde a la flechita arriba
        personaje["rect"].y -= velocidad # Me muevo hacia la arriba (-y)
    if teclas[pygame.K_DOWN]: # Si la tecla corresponde a la flechita abajo
        personaje["rect"].y += velocidad # Me muevo hacia la abajo (+y)

    # --- Colision con los bordes ---
    if personaje["rect"].left < 0: # Si el lado izquierdo del rect de colision es menor que 0
        personaje["rect"].left = 0 # deja al personaje en 0
    if personaje["rect"].right > ancho_pantalla: # Si el lado izquierdo del rect de colision es mayor al ancho de pantalla
        personaje["rect"].right = ancho_pantalla # deja al personaje en el la pos del ancho de pantalla

    if personaje["rect"].top < 0: 
        personaje["rect"].top = 0 
    if personaje["rect"].bottom > alto_pantalla: 
        personaje["rect"].bottom = alto_pantalla 


def dibujar_personaje(pantalla, personaje):
    """
    Dibuja el personaje en la pantalla

    Args:
        pantalla : La superficie de la pantalla
        personaje (dict): Espera el diccionario del personaje
    """
    try:
        if personaje["superficie"]: # Si el personaje posee una superficie
            pantalla.blit(personaje["superficie"], personaje["rect"]) #Entonces, dibujala junto con su rectangulo
    except Exception as e: 
        print("Error al dibujar el personaje: ", e) 
        return None  