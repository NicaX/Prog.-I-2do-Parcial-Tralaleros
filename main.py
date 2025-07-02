 # ----------------- IMPORTS -----------------
import pygame
import sys


# Importamos los módulos y le asignamos un alias
import funciones as f
import interfaz as i
import personaje as p


pygame.init() #Inicializo Pygame
pygame.mixer.init() # Inicializo el mixer de sonido

# ----------------- BUCLE PRINCIPAL (jugar) -----------------
def jugar():
    """
    Función principal que contiene la lógica completa del juego
    Configura la pantalla, carga recursos, maneja eventos y actualiza el estado del juego
    """
    ANCHO = 800 #Asigno valor de px al Ancho de la pantalla
    ALTO = 600 #Asigno valor de px al Alto de la pantalla
    VENTANA = pygame.display.set_mode((ANCHO, ALTO)) #Seteo el tamaño la pantalla
    
    ICONO = f.cargar_imagen("icono.png", 32, 32) # Uso la funcion de cargar imagen para cargar el icono
    pygame.display.set_icon(ICONO) #Seteo el icono
    pygame.display.set_caption("El Ahorcado Tralalero") #Seteo el nombre de la ventana
 
    # ----------------- COLORES -----------------
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)
    VERDE = (0, 255, 0)

    
    # ----------------- INICIALIZACIONES -----------------
    
    lista_palabras = [] #Lista vacia para las palabras del txt
    f.cargar_palabras(lista_palabras) #Uso la funcion cargar palabras para cargar la lista vacia
    palabra_secreta_x_letras, palabra_secreta = f.elegir_palabra(lista_palabras) # Asigno 2 variables, una para la lista que devuelve la palabra por letras y la otra devuelve la palabra completa
    
    letras_adivinadas = [] # Lista vacia para guardas las letras que se adivinaron
    letras_intentadas = [] # Lista vacia para las letras que intentó el usuario
    errores = 0 #Inicializo los errores en 0
    maximo_errores = 6 # Seteo el maximo de errores a 6
    mostrar_mensaje_hasta = 0 #Acumula el tiempo que durará el mensaje en pantalla

    #Inicializo la musica de fondo
    musica = f.cargar_sonido('musica.wav') # Uso la funcion cargar sonido, para cargar la musica de fondo
    musica.play() # Le pongo play a la musica
    musica.set_volume(0.2) # Bajo el volumen de la cancion

    # -------------- BANDERAS --------------
    repetido = False #Bandera para saber si se repitió una letra y mostrar el mensaje de advertencia
    numero = False # Bandera para saber si se ingresó un numero y mostrar el mensaje de advertencia
    mostrar_pantalla_juego = False #Bandera para dibujar la pantalla de juego
    juego_terminado = False #Bandera para cuando termine el juego
    reinciar_juego = False #Bandera para el reinicio del juego (reinicio de variables)

    jugando = True # Bandera para activar o desactivar el bucle principal

    # Crea el personaje guardandolo en la variable
    personaje = p.crear_personaje() 

    reloj = pygame.time.Clock() #Creamos el reloj para los FPS
    

    # Bucle principal del juego
    while jugando: 
        VENTANA.fill(BLANCO) #Rellena pantalla de color BLANCO

        mostrar_pantalla_juego = True #Dibujamos la pantalla
        

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: #Evento de cerrar ventana
                jugando = False #Paro el bucle

            elif evento.type == pygame.KEYDOWN: #Evento de presion de tecla
                # Si el juego ya terminó y está esperando para cerrar, solo permite ESC
                if juego_terminado:

                    if evento.key == pygame.K_ESCAPE: #Evento de presion de la tecla ESC
                        jugando = False
                    continue # No procesar otras teclas si el juego ya terminó

                if evento.key == pygame.K_ESCAPE: 
                    jugando = False 
                    
                elif evento.unicode.isalpha(): #Se verifica se se presiona una tecla de la A a la Z
                    letra_ingresada = evento.unicode.upper() #Paso la letra a mayuscula en caso de que no lo esté
                    
                    if letra_ingresada in letras_intentadas: #Si la letra ingresada ya se ingresó anteriormente
                        mostrar_mensaje_hasta = pygame.time.get_ticks() + 2000 #Seteo mostrar mensaje en 2segundos
                        repetido = True 
                    else:
                        #Sumo los errores, la funcion verificar letra devuelve la cantidad de errores
                        errores = f.verificar_letra(letra_ingresada,palabra_secreta_x_letras,letras_adivinadas,letras_intentadas,errores) 

                #Se agrega está verificación para que no tome como error las flechas que mueven el personaje
                elif evento.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT): 
                    pass #Se ignoran las flechitas
                else: #Si no,
                    mostrar_mensaje_hasta = pygame.time.get_ticks() + 2000 #Seteo mostrar mensaje en 2segundos
                    numero = True # Toqué un numero y me dará una advertencia


        # Dibujamos la pantalla de Juego

        if mostrar_pantalla_juego: #Si la bandera es True
            p.dibujar_personaje(VENTANA, personaje) #Dibujamos el personaje (Tralalero)
                        
            # Solo mueve el personaje si el juego no ha terminado
            if not juego_terminado:
                p.mover_personaje(personaje, ANCHO, ALTO) 

                # Dibuja los elementos del juego (palabra, ahorcado, letras usadas)
                i.dibujar_juego(letras_adivinadas, errores, VENTANA, palabra_secreta_x_letras, letras_intentadas, ANCHO, ALTO, NEGRO) 


                #----------------------------------------------#
                tiempo_actual = pygame.time.get_ticks()

                #Creamos la lógica para mostrar los mensajes de error en pantalla
                if tiempo_actual < mostrar_mensaje_hasta and numero: #Si el tiempo actual es menor al tiempo seteado (2s) y se presiono un numero
                    i.dibujar_texto(VENTANA,"Error, tenés que ingresar letras unicamente",30, ROJO,100,480) # Muestro el error
                else:
                    numero = False #Pasa a reiniciar la bandera

                if tiempo_actual < mostrar_mensaje_hasta and repetido: #Si el tiempo actual es menor al tiempo seteado (2s) y se repitio la letra
                    i.dibujar_texto(VENTANA,"Error, ya ingresaste esa letra rufián",30, ROJO,100,510) # Muestro el error
                else:
                    repetido = False #Pasa a reiniciar la bandera

                #-----------------------------------------------#


                # Verifica si el jugador ganó
                ganado = True #Inicializo la bandera ganado y la verifico enseguida
                for letra in palabra_secreta_x_letras: #Recorro las letras en la lista de letras de la palabra al azar
                    if letra not in letras_adivinadas: #Si la letra no se adivinó aún
                        ganado = False #No gané
                        break

                if ganado: # Pero si no pasó a false en el bucle anterior
                    juego_terminado = True  #Entonces gane :)                 

                elif errores >= maximo_errores: #Si llegué a los errores permitidos
                    juego_terminado = True #Perdí :(                  




# ---- Pantalla de juego terminado donde muestra si ganó o perdio ---- #
            if juego_terminado:
                # Redibuja el estado final para asegurar que el mensaje se vea bien
                i.dibujar_juego(letras_adivinadas, errores, VENTANA, palabra_secreta_x_letras, letras_intentadas, ANCHO, ALTO, NEGRO) 
                musica.stop() #Detengo la musica si se termino el juego
                
                if ganado:
                    i.dibujar_texto(VENTANA, "¡GANASTE!",50, VERDE, 275 , 290)
                    boton_salir, boton_reintentar = i.dibujar_botones_final(VENTANA, ANCHO, BLANCO, NEGRO)
                elif errores >= maximo_errores:
                    i.dibujar_texto(VENTANA, "¡PERDISTE!",50,ROJO, 275 , 290) 
                    i.dibujar_texto(VENTANA, f"La palabra correcta era: {palabra_secreta}", 30, NEGRO , ANCHO // 3 - (len(palabra_secreta_x_letras) * 10), ALTO // 2 + 40)
                    boton_salir, boton_reintentar = i.dibujar_botones_final(VENTANA, ANCHO, BLANCO, NEGRO)

                if evento.type == pygame.MOUSEBUTTONDOWN and juego_terminado : #Evento de click del mouse
                    posicion = evento.pos # Guardo la posicion del mouse
                    if boton_reintentar.collidepoint(posicion) and evento.button == 1: #Si toco el collider del boton reintentar con el boton izquierdo del mouse
                        reinciar_juego = True #Paso a reiniciar el juego
                        mostrar_pantalla_juego = False
                    elif boton_salir.collidepoint(posicion) and evento.button == 1: #Si toco el collider del boton salir con el boton izquierdo del mouse
                        jugando = False # Salgo del juego (del bucle)

               
            # ---- Se reinician las variables cuando el mouse tocó el boton reiniciar ---- #
            if reinciar_juego:

                """Resetea todas las variables del juego a su estado inicial"""

                mostrar_pantalla_juego = True

                musica.play() #Reinicio la musica
                musica.set_volume(0.2)

                # Vuelvo a cargar palabras y elegir nueva palabra
                lista_palabras = []
                f.cargar_palabras(lista_palabras)
                palabra_secreta_x_letras, palabra_secreta = f.elegir_palabra(lista_palabras)

                # Vuelvo a cero las variables
                letras_adivinadas = []
                letras_intentadas = []
                errores = 0
                juego_terminado = False
                ganado = False
                mostrar_mensaje_hasta = 0
                numero = False
                repetido = False
                reinciar_juego = False

                # Reinicio personaje
                personaje = p.crear_personaje()
        
        # Actualiza toda la pantalla para mostrar los cambios
        pygame.display.update()
        # Seteo los FPS
        reloj.tick(60) 

    # Cuando el bucle principal termina (el jugador sale, gana, pierde o tiempo agotado)
    pygame.quit()
    sys.exit()

# ---- Llamamos a la funcion jugar ---- #
jugar()