from cgitb import text
from typing import Self
import pygame
import sys
from pygame.locals import *
from pygame.sprite import collide_mask
import random

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (128, 128, 128)  # Nuevo color para el botón desactivado

# Definir algunas constantes
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SPRITE_SIZE = 32
SPRITE_SCALE = 10  # Escala del sprite (200%)
SPRITE_SHEET = "huevonaranja.png"
FPS = 30

# Inicializar Pygame
pygame.init()

# Cargar la sprite sheet
sprite_sheet = pygame.image.load(SPRITE_SHEET)

# Obtener los cuadros de la sprite sheet y escalarlos
frames = []
for y in range(0, sprite_sheet.get_height(), SPRITE_SIZE):
    for x in range(0, sprite_sheet.get_width(), SPRITE_SIZE):
        frame = sprite_sheet.subsurface(pygame.Rect(x, y, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, (SPRITE_SIZE * SPRITE_SCALE, SPRITE_SIZE * SPRITE_SCALE))
        frames.append(frame)

# Configurar la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Note Pet")

# Establecer el reloj para controlar la velocidad de la animación de los sprites
sprite_clock = pygame.time.Clock()

# Establecer el reloj para controlar la lógica del juego
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
        self.frame_end = 3  # Frame de finalización en la sprite sheet
        self.sprite_time_elapsed = 0  # Tiempo transcurrido para actualizar el sprite
        self.experiencia = 0
        self.nivel = 1  # Nivel inicial
        self.mensaje = Mensaje("")
        self.evoluciones = (2,4,5,7,8)
        self.frames_evolucion = [(0, 3), (4, 7), (8, 11), (12,15), (16,19)]  # Por ejemplo, cada evolución cambia cada 4 frames
        self.evolucion_actual = 0
        self.coins = 0

    def subir_nivel(self):
       if self.experiencia >= 100:  # Verificar si la experiencia alcanzó o superó 100
         niveles_subidos = self.experiencia // 100  # Calcular cuántos niveles se han subido
         self.nivel += niveles_subidos  # Sumar el número de niveles subidos al nivel actual
         self.experiencia %= 100  # Modificar la experiencia para que sea el resto después de subir de nivel
         self.coins += niveles_subidos * 5  # Ajusta este valor según lo que consideres apropiado
         print(f"Felicidades, has subido {niveles_subidos} niveles.")
         print(f"Has conseguido el nivel {self.nivel}")
         print(f"Has ganado {niveles_subidos * 5} coins.")
         print(f"Experiencia total de la mascota: {self.experiencia}")
         


    def update(self, dt):
        # Actualizar el tiempo transcurrido para el sprite
        self.sprite_time_elapsed += dt
        if self.nivel == self.evoluciones[self.evolucion_actual]:
            # Cambiar los frames de acuerdo a la siguiente evolución
            self.frame_start, self.frame_end = self.frames_evolucion[self.evolucion_actual]
            self.evolucion_actual += 1  # Moverse a la siguiente evolución
        if self.evolucion_actual >= len(self.evoluciones):
                self.evolucion_actual = len(self.evoluciones) -1  # Mantener la última evolución
                       
                 
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
        self.duracion_maxima = 3  # Duración máxima del mensaje en segundos

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

        # Función para alimentar a la mascota
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
            dt = game_clock.tick(FPS) / 10000.0  # Control del tiempo del juego
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ingresando = False
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Restaurar tamaño original de la ventana
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        ingresando = False
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Restaurar tamaño original de la ventana
                    elif evento.key == pygame.K_BACKSPACE:
                        self.texto_ingresado = self.texto_ingresado[:-1]
                        pantalla_registro.fill(NEGRO)  # Limpiar la pantalla antes de volver a dibujar el texto
                        texto_superficie = fuente.render(self.texto_ingresado, True, BLANCO)
                        pantalla_registro.blit(texto_superficie, (10, 10))  # Mostrar el texto actualizado
                        pygame.display.flip()  # Actualizar la pantalla
                    elif evento.key == pygame.K_TAB:
                        self.texto_ingresado += '\n'  # Agregar un salto de línea al texto ingresado
                    else:
                        self.texto_ingresado += evento.unicode
                        pantalla_registro.fill(NEGRO)  # Limpiar la pantalla antes de volver a dibujar el texto
                        texto_superficie = fuente.render(self.texto_ingresado, True, BLANCO)
                        pantalla_registro.blit(texto_superficie, (10, 10))  # Mostrar el texto actualizado
                        pygame.display.flip()  # Actualizar la pantalla
                       # Dividir el texto en líneas
            lineas = [self.texto_ingresado[i:i+30] for i in range(0, len(self.texto_ingresado), 30)]
            # Renderizar y mostrar cada línea
            for i, linea in enumerate(lineas):
                texto_superficie = fuente.render(linea, True, BLANCO)
                pantalla_registro.blit(texto_superficie, (10, 10 + i * 24))  # Ajustar la posición vertical
            pygame.display.flip()
                                           
          # Guardar texto en un archivo de texto
        with open("registro_mascota.txt", "a") as archivo:
            archivo.write(self.texto_ingresado + "\n")
                    #Activar reloj principal  
            
dt = game_clock.tick(FPS) / 1000.0  # Convertir a segundos 

# Inicializar mascota
mascota = Mascota()

# Inicializar fuente para mostrar el nivel de hambre y vida
fuente = pygame.font.SysFont("Consolas", 24)
##Clase para iniciar la tienda##

class Shop:
    def __init__(self,mascota):
        self.productos = {
            "zanahoria": {"cantidad": 1, "precio": 1, "imagen": pygame.image.load("zanahoria.png")},
            "naranja": {"cantidad": 3, "precio": 7 , "imagen": pygame.image.load("naranja.png")},
             "muslito": {"cantidad": 1, "precio": 10 , "imagen": pygame.image.load("muslito.png")}
        }
        self.inventario = {}  # Inventario del jugador
        self.mascota = mascota  # Referencia a la mascota
        self.comercio_imagen = pygame.image.load("comercio.png")  # Agregar imagen del comerciante
    def actualizar_coins(self, coins):
        self.coins = coins
        
        
    def dibujar_productos(self, screen):
        # Dibujar botones para cada producto
        boton_posicion = (1, 1)
        for nombre, producto in self.productos.items():
            # Obtener el rectángulo del botón
            producto_rect = producto["imagen"].get_rect(topleft=boton_posicion)
            producto["rect"] = producto_rect  # Guardar el rectángulo en el diccionario del producto
            screen.blit(producto["imagen"], producto_rect)
            texto_producto = fuente.render(f"{nombre} - {producto['precio']} coins", True, BLANCO)
            screen.blit(texto_producto, (producto_rect.x, producto_rect.y + 40))
            boton_posicion = (boton_posicion[0], boton_posicion[1] + 70)
            
            ##Monedas##
            monedas_imagen = pygame.image.load("monedas.png")
            monedas_x = 300  # Coordenada x de las monedas
            monedas_y = 460 # Coordenada y de las monedas
            screen.blit(monedas_imagen, (monedas_x, monedas_y))
    
    # Mostrar cantidad de monedas de la mascota
            texto_monedas = fuente.render(f"coins: {mascota.coins}", True, BLANCO)
            screen.blit(texto_monedas, (monedas_x + 40, monedas_y + 5))
    #dibujar comerciante
        comercio_rect = self.comercio_imagen.get_rect(topleft=(240, 460))
        screen.blit(self.comercio_imagen, comercio_rect)
        
        return comercio_rect  # Devolver el rectángulo del botón de comercio



    def comprar_producto(self, nombre):
        if nombre in self.productos:
            producto = self.productos[nombre]
            if self.mascota.coins >= producto["precio"]:
                # Restar el precio del producto de las monedas de la mascota
                self.mascota.coins -= producto["precio"]
                # Agregar el producto al inventario de la mascota
                if nombre in self.inventario:
                    self.inventario[nombre] += 1
                else:
                    self.inventario[nombre] = 1
                print(f"Has comprado {nombre}")
                print(f"Monedas restantes de la mascota: {self.mascota.coins}")
                if nombre == "naranja":
                 self.mascota.experiencia += 40  # Ajusta este valor según lo que consideres apropiado
                 print("Has ganado experiencia por comprar una naranja")
                 print(f"Experiencia total de la mascota: {self.mascota.experiencia}")
                 self.mascota.subir_nivel()  # Verificar si se puede subir de nivel
                elif nombre == "zanahoria":
                 self.mascota.vida += 20 #Ajustar el valor de acurdo a lo apropiado
                 print("has ganado vida por comprar una zanahoria")
                 print(f"Vida total de la mascota:{self.mascota.vida}")
                elif nombre == "muslito":
                 self.mascota.hambre += 90 #Ajustar el valor de acurdo a lo apropiado
                 print("has alimentado a la mascota con un muslito")
                 print(f"hambre total de la mascota:{self.mascota.hambre}")
            else:
                print("No tienes suficientes monedas")
                print(self.inventario)
        else:
            print("Producto no encontrado")
            
    def comerciar(self):
        # Obtener un producto aleatorio del inventario
        if self.inventario:
            producto_aleatorio = random.choice(list(self.inventario.keys()))
            cantidad_producto = self.inventario[producto_aleatorio]
            # Obtener monedas al vender el producto (aquí puedes ajustar cómo se calculan las monedas)
            monedas_obtenidas = random.randint(1, 3) * cantidad_producto
            # Actualizar el inventario y las monedas del jugador
            del self.inventario[producto_aleatorio]  # Eliminar el producto del inventario
            self.mascota.coins += monedas_obtenidas  # Agregar las monedas al jugador
            print(f"Has vendido {cantidad_producto} {producto_aleatorio} por {monedas_obtenidas} monedas.")
        else:
            print("No tienes productos para comerciar.")
            


    def ingresar_shop(self):
        pygame.display.set_caption("Tienda de Mascota")
        pantalla_shop = pygame.display.set_mode((500, 500))
        ingresando_shop = True
        sonidoopen.play()

        while ingresando_shop:
            dt = game_clock.tick(FPS) / 10000.0  # Control del tiempo del juego
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ingresando_shop = False
                    pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT))  # Restaurar tamaño original de la ventana
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  # Boton izquierdo del raton
                        # Verificar si se hizo clic en un producto y comprarlo
                        for nombre, producto in self.productos.items():
                            if producto["rect"].collidepoint(evento.pos):
                                self.comprar_producto(nombre)
                        comercio_rect = self.comercio_imagen.get_rect(topleft=(240, 460))
                    if comercio_rect.collidepoint(evento.pos):
                        self.comerciar()
                        mascota.subir_nivel()
            pantalla_shop.fill(NEGRO)
            self.dibujar_productos(pantalla_shop)  # Dibujar los productos en la tienda
            pygame.display.flip()

    dt = game_clock.tick(FPS) / 1000.0  # Convertir a segundos 
        # Actualizar la mascota
    mascota.update(dt)


# Inicializar botón de alimentar
boton_alimentar = pygame.Rect(450, 80, 140, 40)
###


# Inicializar el objeto de registro de texto
registro = Registro()
# Iniciaalizar el objetode tienda de mascota

shop = Shop(mascota)

# Inicializar el tiempo transcurrido
time_elapsed = 0

# Variable para controlar si se debe bloquear el botón de alimentar
bloquear_boton_alimentar = False

#sonidos##

sonidoopen =pygame.mixer.Sound("open.mp3")

# Función para cargar datos al iniciar el juego
def cargar_datos():
    try:
        with open("save.pet.txt", "r") as archivo:
            # Leer las primeras 9 posiciones para los valores de la mascota
            datos_mascota = archivo.readline().strip().split(',')
            mascota.hambre = float(datos_mascota[0])
            mascota.vida = float(datos_mascota[1])
            mascota.experiencia = int(datos_mascota[2])
            mascota.nivel = int(datos_mascota[3])
            mascota.evolucion_actual = int(datos_mascota[4])
            mascota.frame_index = int(datos_mascota[5])
            mascota.frame_start = int(datos_mascota[6])
            mascota.frame_end = int(datos_mascota[7])
            mascota.coins = int(datos_mascota[8])
                       
    except FileNotFoundError:
        # Manejar el caso cuando el archivo no existe
        pass

def cargar_inventario():
    try:
        with open("inventory.txt", "r") as archivo:
            for linea in archivo:
                nombre, cantidad = linea.strip().split(',')
                shop.inventario[nombre] = int(cantidad)
    except FileNotFoundError:
        # Manejar el caso cuando el archivo no existe
        pass

# Llamada a la función para cargar datos al iniciar el juego
cargar_datos()

############ llamar funcion cargar inventario###
cargar_inventario()

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                if not mascota.muerto and not bloquear_boton_alimentar and boton_alimentar.collidepoint(event.pos):
                    alimentar_mascota(mascota)
                elif not mascota.muerto:
                    mascota.experiencia += 1  # Incrementar experiencia al hacer clic
                    print(f"Has ganado 1 punto de experiencia Total de experiencia: {mascota.experiencia}")
                    mascota.subir_nivel()  # Verificar si se puede subir de nivel
            elif event.button == 3:  # Botón derecho del ratón
                if not mascota.muerto:
                    registro.ingresar_texto()
            elif event.button == 2:  # Botón central del ratón
                if not mascota.muerto:
                    shop.ingresar_shop()  

    # Calcular el tiempo transcurrido desde el último fotograma
    dt = game_clock.tick(FPS) / 1000.0  # Se fijan los FPS a 30
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

        # Lógica para abrir la ventana de texto cada 10 minutos
        if time_elapsed > 600:
            registro.ingresar_texto()
            time_elapsed = 0  # Reiniciar el tiempo transcurrido

        # Actualizar la mascota
        mascota.update(dt)
        # Actualizar el mensaje
        mascota.mensaje.actualizar(dt)
    else:
        # Si la mascota está muerta, bloquear el botón de alimentar durante 2 minutos
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
            mascota.evolucion_actual = 1
            mascota.coins = 0
            mascota.frames_evolucion = 0,3
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

    # Dibujar botón de alimentar centrado en la parte inferior de la pantalla
    boton_alimentar.x = (SCREEN_WIDTH - boton_alimentar.width) // 2
    boton_alimentar.y = SCREEN_HEIGHT - 80  # Ajustar la posición vertical
    pygame.draw.rect(screen, BLANCO if not bloquear_boton_alimentar else GRIS, boton_alimentar)  # Cambiar el color si está bloqueado

    # Definir el texto del botón según el estado de la mascota
    if mascota.muerto:
        texto_boton = fuente.render("Muerto", True, NEGRO)
    elif bloquear_boton_alimentar:
        texto_boton = fuente.render("Bloqueado", True, ROJO)
    else:
        texto_boton = fuente.render("Alimentar", True, NEGRO)

    # Mostrar el texto del botón
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
        archivo.write(f"{mascota.hambre},{mascota.vida},{mascota.experiencia},{mascota.nivel},{mascota.evolucion_actual},{mascota.frame_index},{mascota.frame_start},{mascota.frame_end},{mascota.coins}")
# Guardar datos del inventario
def guardar_inventario():
    with open("inventory.txt", "w") as archivo:
        for nombre, cantidad in shop.inventario.items():
            archivo.write(f"{nombre},{cantidad}\n")


# Guardar datos del inventario
guardar_inventario()       

# Llamada a la función para guardar datos antes de cerrar el juego
guardar_datos()

# Luego de salir del bucle principal, cerrar Pygame
pygame.quit()
sys.exit()