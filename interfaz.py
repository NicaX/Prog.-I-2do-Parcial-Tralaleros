import pygame

def dibujar_botones_final(pantalla, ancho_pantalla, color_fondo, color_texto):
    """
        Dibuja los botones finales de Reinciar el juego o Salir del juego

    Args:
        pantalla : La superficie de la pantalla
        ancho_pantalla : Recibe el valor del ancho de pantalla
        color_fondo : Color relleno del boton
        color_texto : Color del texto del boton


    """
    ancho_boton = 120 #Asigno el ancho del boton
    alto_boton = 40 #Asigno el alto del boton
    posicion_y = 25

    try: 

        boton_reintentar = pygame.Rect(20, posicion_y, ancho_boton, alto_boton) #Creo el rectangulo que colisiona
        pygame.draw.rect(pantalla, color_fondo, boton_reintentar) #Dibujo el rectangulo pasandole el boton reintentar (colisonador)  
    
        boton_salir = pygame.Rect(ancho_pantalla - 90, posicion_y, ancho_boton, alto_boton) #Creo el rectangulo que colisiona
        pygame.draw.rect(pantalla, color_fondo, boton_salir) #Dibujo el rectangulo pasandole el boton salir (colisonador)  
        

        dibujar_texto(pantalla, "Reintentar", 25, color_texto, 20, posicion_y)  # Dibujo el texto Reintentar encima del collider
        dibujar_texto(pantalla, "Salir", 25, color_texto, ancho_pantalla - 90, posicion_y) # Dibujo el texto Salir encima del collider
        
        return boton_salir, boton_reintentar

    except Exception as e:
        print("Error al dibujar los botones: " , e)
        return None, None




def dibujar_texto(pantalla, texto, tamaño, color, x, y):
    """
        Dibuja el texto en pantalla

    Args:
        pantalla : La superficie de la pantalla
        texto (str): El texto
        tamaño (int): Tamaño de la letra
        color :  Color del texto
        x (int): La coordenada X superior izquierda del texto.
        y (int): La coordenada Y superior izquierda del texto.
    """
    fuente = pygame.font.SysFont("arial", tamaño) #Asigno que fuente y su tamaño
    superficie_texto = fuente.render(texto, True, color) #Renderizo el texto, lo suavizo y le paso el color
    rect_texto = superficie_texto.get_rect() # Le asigno un rectangulo
    rect_texto.topleft = (x, y) #Para asignarle la posicion x e y del texto
    pantalla.blit(superficie_texto, rect_texto) #Lo dibujamos :)

def dibujar_palabra_actual(pantalla, letras, letras_adivinadas): 
    """
        Dibuja la palabra secreta con las letras adivinadas visibles y los guiones para las no adivinadas

    Args:
        ppantalla : La superficie de la pantalla
        palabra (list): Espera la lista de palabras
        letras_adivinadas (list): Espera la lista de letras adivinadas
    """
    letra_en_pantalla = "" #Inicializo variable con string vacio
    for letra in letras: #Se recorren las letras en letras (la lista de letras)
        if letra in letras_adivinadas: #Si la letra está en la lista de letras adivinadas (lista de letras adivinadas)
            letra_en_pantalla += letra + " " #Se muestra la letra adivinada en pantalla y se agrega un espacio
        else: #Si no
            letra_en_pantalla += "_ " #Muestro un guion bajo con espacio
    
    dibujar_texto(pantalla, letra_en_pantalla, 40, (0, 0, 0), 100, 400)

def dibujar_letras_usadas(pantalla, letras_usadas):
    """
        Dibuja las letras que el jugador ya ha intentado.

    Args:
        pantalla : La superficie de la pantalla
        letras_usadas (list): Espera la lista de letras ingresadas por el usuario
    """
    texto = "Letras usadas: " + " ".join(letras_usadas) 
    dibujar_texto(pantalla, texto, 30, (100, 0, 0), 100, 450)

def dibujar_estructura(pantalla):
    """
    Dibuja la estructura base del ahorcado.

    Args:
        pantalla : La superficie de la pantalla
    """
    color = (0, 0, 0) # Negro
    pygame.draw.line(pantalla, color, (90, 310), (210, 310), 22) 
    pygame.draw.line(pantalla, color, (100, 300), (200, 300), 22) # Base
    pygame.draw.line(pantalla, color, (150, 300), (150, 111), 10) # Poste vertical
    pygame.draw.line(pantalla, color, (150, 300), (150, 270), 30) # Poste vertical
    pygame.draw.line(pantalla, color, (150, 300), (150, 280), 50) # Poste vertical
    pygame.draw.line(pantalla, color, (130, 100), (170, 100), 35) # Esquinero
    pygame.draw.line(pantalla, color, (150, 100), (255, 100), 12) # Barra horizontal
    pygame.draw.line(pantalla, color, (250, 100), (250, 130), 4) # Cuerda

def dibujar_cuerpo(pantalla, errores):
    """
        Dibuja el cuerpo si el usuario comete errores
    Args:
        pantalla : La superficie de la pantalla
        errores (int): Contador de errores
    """
    color = (0, 0, 0) # Negro
    if errores > 0:
        pygame.draw.circle(pantalla, color, (250, 150), 20, 2) # Cabeza
    if errores > 1:
        pygame.draw.line(pantalla, color, (250, 170), (250, 220), 2) # Cuerpo
    if errores > 2:
        pygame.draw.line(pantalla, color, (250, 180), (230, 200), 2) # Brazo izquierdo
    if errores > 3:
        pygame.draw.line(pantalla, color, (250, 180), (270, 200), 2) # Brazo derecho
    if errores > 4:
        pygame.draw.line(pantalla, color, (250, 220), (230, 250), 2) # Pierna izquierda
    if errores > 5:
        pygame.draw.line(pantalla, color, (250, 220), (270, 250), 2) # Pierna derecha

def dibujar_juego(letras_adivinadas, errores, pantalla, palabra_secreta_x_letras, letras_intentadas, ancho_pantalla, alto_pantalla, color_texto=(0, 0, 0)):
    """
    Dibuja todos los elementos visuales del juego principal (excepto el personaje).

    Args:
        letras_adivinadas (list): Espera la lista de las letras adivinadas
        errores (int): Contador de errores
        pantalla : La superficie de la pantalla
        palabra_secreta_x_letras (list): La palabra secreta como lista de letras
        letras_intentadas (list): Todas las letras que se han intentado
        ancho_pantalla (int): Ancho de la pantalla
        alto_pantalla (int): Alto de la pantalla
        color_texto : Color del texto
    """
    # Dibuja el título del juego y una breve explicación.
    dibujar_texto(pantalla, "El Ahorcado Tralalero", 50, color_texto, ancho_pantalla // 2 - 250, 10) 
    dibujar_texto(pantalla, "Adivina la palabra antes de que te ahorquen", 20, color_texto, ancho_pantalla // 2 - 200, 65) 
    dibujar_texto(pantalla, "Presiona una letra para adivinar", 30, (0, 0, 0), ancho_pantalla // 2 - 200, alto_pantalla - 50) 

    dibujar_estructura(pantalla) 
    dibujar_cuerpo(pantalla, errores) 
    dibujar_palabra_actual(pantalla, palabra_secreta_x_letras, letras_adivinadas) 
    dibujar_letras_usadas(pantalla, letras_intentadas) 
    
