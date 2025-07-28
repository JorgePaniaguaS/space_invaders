import pygame
import random
import math
import sys

# Inicialización
pygame.init()
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FPS = 60

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
AZUL = (100, 100, 255)

# Cargar sprites desde imágenes externas
jugador_img = pygame.image.load("player.png").convert_alpha()
jugador_img = pygame.transform.scale(jugador_img, (48, 48))

bala_img = pygame.image.load("bullet.png").convert_alpha()
bala_img = pygame.transform.scale(bala_img, (8, 16))

enemigo_img = pygame.image.load("enemy.png").convert_alpha()
enemigo_img = pygame.transform.scale(enemigo_img, (32, 32))

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)

# Variables globales
dificultad = "Seleccionando"
velocidad_enemigo = 2


def mostrar_texto(texto, x, y, fuente, color=BLANCO):
    t = fuente.render(texto, True, color)
    pantalla.blit(t, (x, y))


def boton(texto, x, y, w, h, accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    dentro = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = AZUL if dentro else (50, 50, 200)
    pygame.draw.rect(pantalla, color, (x, y, w, h))
    mostrar_texto(texto, x + 10, y + 10, fuente)
    if dentro and click[0] and accion:
        pygame.time.wait(200)
        accion()


def set_dificultad(dif):
    global dificultad, velocidad_enemigo
    dificultad = dif
    if dif == "Fácil":
        velocidad_enemigo = 2
    elif dif == "Normal":
        velocidad_enemigo = 4
    elif dif == "Difícil":
        velocidad_enemigo = 6
    elif dif == "Extremo":
        velocidad_enemigo = 8
        


def seleccionar_dificultad():
    global dificultad
    seleccionando = True
    while seleccionando:
        pantalla.fill(NEGRO)
        mostrar_texto("Selecciona dificultad", 200, 100, fuente_grande)

        boton("Fácil", 300, 200, 200, 50, lambda: set_dificultad("Fácil"))
        boton("Normal", 300, 300, 200, 50, lambda: set_dificultad("Normal"))
        boton("Difícil", 300, 400, 200, 50, lambda: set_dificultad("Difícil"))
        boton("Extremo", 300, 500, 200, 50, lambda: set_dificultad("Extremo"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if dificultad != "Seleccionando":
            seleccionando = False

        pygame.display.update()
        clock.tick(30)


def juego():
    jugador_x = 370
    jugador_y = 480
    jugador_x_cambio = 0

    enemigos = []
    for _ in range(6):
        enemigos.append({
            "img": enemigo_img.copy(),
            "x": random.randint(0, 736),
            "y": random.randint(50, 150),
            "x_cambio": velocidad_enemigo,
            "y_cambio": 40
        })

    bala_x = 0
    bala_y = 480
    bala_y_cambio = 20
    bala_estado = "lista"

    puntaje = 0
    game_over = False

    def hay_colision(x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2) < 27

    def disparar_bala(x, y):
        pantalla.blit(bala_img, (x + 20, y))

    def mostrar_game_over():
        pantalla.fill(NEGRO)
        mostrar_texto("GAME OVER", 250, 200, fuente_grande, ROJO)
        mostrar_texto(f"Puntaje final: {puntaje}", 280, 280, fuente)
        boton("Reintentar", 300, 360, 200, 50, lambda: juego())

    ejecutando = True
    while ejecutando:
        pantalla.fill(NEGRO)
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        jugador_x_cambio = -5
                    if evento.key == pygame.K_RIGHT:
                        jugador_x_cambio = 5
                    if evento.key == pygame.K_SPACE and bala_estado == "lista":
                        bala_x = jugador_x
                        bala_estado = "fuego"
                if evento.type == pygame.KEYUP:
                    if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        jugador_x_cambio = 0

        if not game_over:
            jugador_x += jugador_x_cambio
            jugador_x = max(0, min(jugador_x, 752))
            pantalla.blit(jugador_img, (jugador_x, jugador_y))

            for enemigo in enemigos:
                enemigo["x"] += enemigo["x_cambio"]
                if enemigo["x"] <= 0 or enemigo["x"] >= 768:
                    enemigo["x_cambio"] *= -1
                    enemigo["y"] += enemigo["y_cambio"]

                if enemigo["y"] > 440:
                    game_over = True

                if bala_estado == "fuego" and hay_colision(enemigo["x"], enemigo["y"], bala_x, bala_y):
                    bala_y = 480
                    bala_estado = "lista"
                    puntaje += 1
                    enemigo["x"] = random.randint(0, 736)
                    enemigo["y"] = random.randint(50, 150)

                pantalla.blit(enemigo["img"], (enemigo["x"], enemigo["y"]))

            if bala_estado == "fuego":
                disparar_bala(bala_x, bala_y)
                bala_y -= bala_y_cambio
                if bala_y <= 0:
                    bala_y = 480
                    bala_estado = "lista"

            mostrar_texto(f"Puntaje: {puntaje}", 10, 10, fuente)
        else:
            mostrar_game_over()

        pygame.display.update()


# Ejecutar
seleccionar_dificultad()
juego()
