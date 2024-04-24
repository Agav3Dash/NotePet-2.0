
# -*- coding: utf-8 -*-

from cgitb import text
from typing import Self
import pygame
import sys ,os
from pygame.locals import *


# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (128, 128, 128)  # Nuevo color para el bot�n desactivado


# Inicializar Pygame
pygame.init()

# Cargar la sprite sheet
sprite_sheet = pygame.image.load("huevonaranja.png")

# Obtener los cuadros de la sprite sheet y escalarlos
frames = []
for y in range(0, sprite_sheet.get_height(), 32):
    for x in range(0, sprite_sheet.get_width(), 32):
        frame = sprite_sheet.subsurface(pygame.Rect(x, y, 32, 32))
        frame = pygame.transform.scale(frame, (32 * 10, 32 * 10))
        frames.append(frame)

# Configurar la pantalla
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Note Pet")

# Establecer el reloj para controlar la velocidad de la animaci�n de los sprites
sprite_clock = pygame.time.Clock()

# Establecer el reloj para controlar la l�gica del juego
game_clock = pygame.time.Clock()

# Clase para manejar la mascota virtual
class Mascota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = frames[0]  # Seleccionar el primer frame como imagen inicial
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)
        self.hambre = 101
        self.vida = 101
        self.muerto = False
        self.tiempo_muerto = None
        self.frame_index = 0 # Indicador del frame actual
        self.frame_start = 0  # Frame de inicio en la sprite sheet
        self.frame_end = 3  # Frame de finalizaci�n en la sprite sheet
        self.sprite_time_elapsed = 0  # Tiempo transcurrido para actualizar el sprite
        self.experiencia = 0
        self.nivel = 1  # Nivel inicial
        self.mensaje = Mensaje("")
        self.evoluciones = (2,4,5,7,8)
        self.frames_evolucion = [(0, 3), (4, 7), (8, 11), (12,15), (16,19)]  # Por ejemplo, cada evoluci�n cambia cada 4 frames
        self.evolucion_actual = 0

    def subir_nivel(self):
        if self.experiencia >= 100:  # Umbral para subir de nivel
            self.nivel += 1
            print(f"Felicidades Has subido al nivel {self.nivel}")
            self.experiencia = 0  # Reiniciar la experiencia al subir de nivel

    def update(self, dt):
        # Actualizar el tiempo transcurrido para el sprite
        self.sprite_time_elapsed += dt
        if self.nivel == self.evoluciones[self.evolucion_actual]:
            # Cambiar los frames de acuerdo a la siguiente evoluci�n
            self.frame_start, self.frame_end = self.frames_evolucion[self.evolucion_actual]
            self.evolucion_actual += 1  # Moverse a la siguiente evoluci�n
        if self.evolucion_actual >= len(self.evoluciones):
                self.evolucion_actual = len(self.evoluciones) -1  # Mantener la �ltima evoluci�n
                  
        # Actualizar la imagen de la mascota con el nuevo conjunto de frames
          
       

        # Cambiar de frame cada 1 segundos
        if  self.sprite_time_elapsed >= 1:
         self.frame_index = (self.frame_index + 1) % (self.frame_end - self.frame_start + 1) + self.frame_start
         self.image = frames[self.frame_index]  # Asignar el nuevo frame como imagen de la mascota
         self.sprite_time_elapsed = 0  # Reiniciar el tiempo transcurrido para el sprite

            
             #Clase para dar mensajes
class Mensaje:
    def __init__(self, texto):
        self.texto = texto
        self.visible = True
        self.font = pygame.font.SysFont("Consolas", 14)  # Fuente para el mensaje
        self.tiempo_visible = 0  # Tiempo transcurrido con el mensaje visible
        self.duracion_maxima = 3  # Duraci�n m�xima del mensaje en segundos

    def mostrar(self, pantalla, x, y):
        if self.visible:
            texto_surface = self.font.render(self.texto, True, BLANCO)  # Renderizar el texto
            pantalla.blit(texto_surface, (10, 440))  # Mostrar el texto en la pantalla

    def actualizar(self, dt):
        if self.visible:
            self.tiempo_visible += dt
            if self.tiempo_visible >= self.duracion_maxima:
                self.visible = False
                self.tiempo_visible = 0

    def mostrar_mensaje(self, texto):
        self.texto = texto
        self.visible = True
        self.tiempo_visible = 0  # Reiniciar el tiempo visible

        # Funci�n para alimentar a la mascota
def alimentar_mascota(mascota):
    mascota.hambre += 1 #1
    mascota.vida += .2  #.2
    if mascota.hambre > 101:
        mascota.hambre = 101
    if mascota.vida > 101:
        mascota.vida = 101
    mascota.mensaje = Mensaje("Rico taco")
    

# Clase para manejar el registro de texto
class Registro:
    def __init__(self):
        self.texto_ingresado = ""

    def ingresar_texto(self):
        pygame.display.set_caption("Notas de Mascota")
        pantalla_registro = pygame.display.set_mode((500, 500))
        fuente = pygame.font.SysFont("Consolas", 24)
        ingresando = True
        self.texto_ingresado = ""  # Borrar el texto ingresado anteriormente al abrir la pantalla
        sonidoopen.play()

        while ingresando:
            dt = game_clock.tick(30) / 10000.0  # Control del tiempo del juego
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ingresando = False
                    pygame.display.set_mode((500, 500))  # Restaurar tama�o original de la ventana
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        ingresando = False
                        pygame.display.set_mode((500, 500))  # Restaurar tama�o original de la ventana
                    elif evento.key == pygame.K_BACKSPACE:
                        self.texto_ingresado = self.texto_ingresado[:-1]
                        pantalla_registro.fill(NEGRO)  # Limpiar la pantalla antes de volver a dibujar el texto
                        texto_superficie = fuente.render(self.texto_ingresado, True, BLANCO)
                        pantalla_registro.blit(texto_superficie, (10, 10))  # Mostrar el texto actualizado
                        pygame.display.flip()  # Actualizar la pantalla
                    elif evento.key == pygame.K_TAB:
                        self.texto_ingresado += '\n'  # Agregar un salto de l�nea al texto ingresado
                    else:
                        self.texto_ingresado += evento.unicode
                        pantalla_registro.fill(NEGRO)  # Limpiar la pantalla antes de volver a dibujar el texto
                        texto_superficie = fuente.render(self.texto_ingresado, True, BLANCO)
                        pantalla_registro.blit(texto_superficie, (10, 10))  # Mostrar el texto actualizado
                        pygame.display.flip()  # Actualizar la pantalla
                       # Dividir el texto en l�neas
            lineas = [self.texto_ingresado[i:i+30] for i in range(0, len(self.texto_ingresado), 30)]
            # Renderizar y mostrar cada l�nea
            for i, linea in enumerate(lineas):
                texto_superficie = fuente.render(linea, True, BLANCO)
                pantalla_registro.blit(texto_superficie, (10, 10 + i * 24))  # Ajustar la posici�n vertical
            pygame.display.flip()
                                           
          # Guardar texto en un archivo de texto
        with open("registro_mascota.txt", "a") as archivo:
            archivo.write(self.texto_ingresado + "\n")
                    #Activar reloj principal  
            
dt = game_clock.tick(30) / 1000.0  # Convertir a segundos 

# Inicializar mascota
mascota = Mascota()

# Inicializar fuente para mostrar el nivel de hambre y vida
fuente = pygame.font.SysFont("Consolas", 24)

# Inicializar bot�n de alimentar
boton_alimentar = pygame.Rect(450, 80, 140, 40)

# Inicializar el objeto de registro de texto
registro = Registro()

# Inicializar el tiempo transcurrido
time_elapsed = 0

# Variable para controlar si se debe bloquear el bot�n de alimentar
bloquear_boton_alimentar = False

#sonidos##

sonidoopen =pygame.mixer.Sound("open.mp3")

# Funci�n para cargar datos al iniciar el juego
def cargar_datos():
    try:
        with open("save.pet.txt", "r") as archivo:
            datos = archivo.readline().strip().split(',')
            mascota.hambre = float(datos[0])
            mascota.vida = float(datos[1])
            mascota.experiencia = int(datos[2])
            mascota.nivel = int(datos[3])
            mascota.evolucion_actual = int(datos[4])
            mascota.frame_index = int(datos[5])
            mascota.frame_start = int(datos[6])
            mascota.frame_end = int(datos[7])
    except FileNotFoundError:
        # Manejar el caso cuando el archivo no existe
        pass

# Llamada a la funci�n para cargar datos al iniciar el juego
cargar_datos()


# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bot�n izquierdo del rat�n
                if not mascota.muerto and not bloquear_boton_alimentar and boton_alimentar.collidepoint(event.pos):
                    alimentar_mascota(mascota)
                elif not mascota.muerto:
                    mascota.experiencia += 1  # Incrementar experiencia al hacer clic
                    print(f"Has ganado 1 punto de experiencia Total de experiencia: {mascota.experiencia}")
                    mascota.subir_nivel()  # Verificar si se puede subir de nivel
            elif event.button == 3:  # Bot�n derecho del rat�n
                if not mascota.muerto:
                    registro.ingresar_texto()

    # Calcular el tiempo transcurrido desde el �ltimo fotograma
    dt = game_clock.tick(30) / 1000.0  # Se fijan los FPS a 30
    time_elapsed += dt
    # Calcular el nivel actual
    nivel_actual = mascota.nivel + int(mascota.experiencia / 100)

    # Actualizar la vida y el hambre
    if not mascota.muerto:
        mascota.hambre -= dt * .1 # Reducir el hambre con el tiempo .1
        mascota.vida -= dt * .06  # Reducir la vida con el tiempo     .06

        # Restringir los valores de hambre y vida entre 0 y 100
        mascota.hambre = max(0, min(101, mascota.hambre))
        mascota.vida = max(0, min(101, mascota.vida))

        # L�gica para abrir la ventana de texto cada 10 minutos
        if time_elapsed > 600:
            registro.ingresar_texto()
            time_elapsed = 0  # Reiniciar el tiempo transcurrido

        # Actualizar la mascota
        mascota.update(dt)
        # Actualizar el mensaje
        mascota.mensaje.actualizar(dt)
    else:
        # Si la mascota est� muerta, bloquear el bot�n de alimentar durante 2 minutos
        if mascota.tiempo_muerto is None:
            mascota.tiempo_muerto = pygame.time.get_ticks()  # Marcar el tiempo de muerte

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - mascota.tiempo_muerto

        if tiempo_transcurrido > 120000:  # 3600 segundos = 4 minutos
            bloquear_boton_alimentar = False
            mascota.tiempo_muerto = None
            mascota.muerto = False
            mascota.hambre = 20
            mascota.vida = 50
            mascota.nivel = 0
            mascota.experiencia = 0
            mascota.frame_index = 0
            mascota.frame_start = 0
            mascota.frame_end = 3
            mascota.evolucion_actual = 0
            pygame.display.flip()
        else:
            bloquear_boton_alimentar = True

            
        # Actualizar la mascota
        mascota.update(dt)
        # Actualizar el mensaje
        mascota.mensaje.actualizar(dt)
    # Revisar si la mascota ha muerto debido a hambre y vida cero
    if mascota.hambre <= 0 and mascota.vida <= 0:
        mascota.muerto = True
        bloquear_boton_alimentar = True

    # Dibujar la pantalla
    screen.fill(NEGRO)

    # Dibujar la mascota
    screen.blit(mascota.image, mascota.rect)

    # Dibujar barra de hambre
    barra_hambre_ancho = max(mascota.hambre, 0) * 3  # Asegurarse de que la anchura nunca sea negativa
    pygame.draw.rect(screen, VERDE, (10, 10, barra_hambre_ancho, 20))
    pygame.draw.rect(screen, BLANCO, (10, 10, 3, 20), 2)
    texto_hambre = fuente.render(f"Hambre: {int(max(mascota.hambre, 0))}", True, BLANCO)
    screen.blit(texto_hambre, (330, 10))

    # Dibujar barra de vida
    barra_vida_ancho = max(mascota.vida, 0) * 3  # Asegurarse de que la anchura nunca sea negativa
    pygame.draw.rect(screen, ROJO, (10, 40, barra_vida_ancho, 20))
    pygame.draw.rect(screen, BLANCO, (10, 40, 3, 20), 2)
    texto_vida = fuente.render(f"Vida: {int(max(mascota.vida, 0))}", True, BLANCO)
    screen.blit(texto_vida, (330, 40))

    # Dibujar barra de experiencia
    barra_experiencia_ancho = max(mascota.experiencia, 0) * 4.7  # Asegurarse de que la anchura nunca sea negativa
    pygame.draw.rect(screen, AZUL, (10, 470, barra_experiencia_ancho, 20))
    pygame.draw.rect(screen, AZUL, (10, 470, 1, 20), 2)
    texto_experiencia = fuente.render(f"Experiencia: {int(mascota.experiencia)}", True, BLANCO)
    screen.blit(texto_experiencia, (10, 470))
    screen.blit(texto_experiencia, (10, 470))
    
    # Mostrar el nivel actual en la barra de experiencia
    texto_nivel = fuente.render(f"Nivel: {nivel_actual}", True, BLANCO)
    screen.blit(texto_nivel, (360, 470))

    # Dibujar bot�n de alimentar centrado en la parte inferior de la pantalla
    boton_alimentar.x = (500 - boton_alimentar.width) // 2
    boton_alimentar.y = 500 - 80  # Ajustar la posici�n vertical
    pygame.draw.rect(screen, BLANCO if not bloquear_boton_alimentar else GRIS, boton_alimentar)  # Cambiar el color si est� bloqueado

    # Definir el texto del bot�n seg�n el estado de la mascota
    if mascota.muerto:
        texto_boton = fuente.render("Muerto", True, NEGRO)
    elif bloquear_boton_alimentar:
        texto_boton = fuente.render("Bloqueado", True, ROJO)
    else:
        texto_boton = fuente.render("Alimentar", True, NEGRO)

    # Mostrar el texto del bot�n
    screen.blit(texto_boton, (boton_alimentar.x + 10, boton_alimentar.y + 10))

    # Mostrar mensajes
    mascota.mensaje.mostrar(screen, 10, 100)

    # Actualizar la pantalla
    pygame.display.flip()


    # Mostrar mensajes
    mascota.mensaje.mostrar(screen, 10, 100)
    pygame.display.flip()


# Guardar datos antes de cerrar el juego
def guardar_datos():
    with open("save.pet.txt", "w") as archivo:
        archivo.write(f"{mascota.hambre},{mascota.vida},{mascota.experiencia},{mascota.nivel},{mascota.evolucion_actual},{mascota.frame_index},{mascota.frame_start},{mascota.frame_end}")

# Llamada a la funci�n para guardar datos antes de cerrar el juego
guardar_datos()

# Luego de salir del bucle principal, cerrar Pygame
pygame.quit()
sys.exit()