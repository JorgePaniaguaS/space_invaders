import pygame
import random
import math
import sys
import os

# Ajusta el directorio de trabajo a la ubicación del archivo .py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
AZUL = (100, 100, 255)
AMARILLO = (255, 255, 0)

# Carga la imagen indicada o genera un gráfico básico si no la encuentra
def cargar_o_crear_sprite(nombre_archivo, ancho, alto, color_respaldo, forma="rect"):
    try:
        img = pygame.image.load(nombre_archivo).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    except (pygame.error, FileNotFoundError):
        surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        if forma == "triangulo":
            pygame.draw.polygon(surf, color_respaldo, [(ancho // 2, 0), (0, alto), (ancho, alto)])
        elif forma == "circulo":
            pygame.draw.circle(surf, color_respaldo, (ancho // 2, alto // 2), min(ancho, alto) // 2)
        else:
            surf.fill(color_respaldo)
        return surf

# Cargar sprites (usa la imagen .png si existe, o dibuja una forma de respaldo)
jugador_img = cargar_o_crear_sprite("player.png", 48, 48, VERDE, forma="triangulo")
bala_img = cargar_o_crear_sprite("bullet.png", 8, 16, AMARILLO, forma="rect")
enemigo_img = cargar_o_crear_sprite("enemy.png", 32, 32, ROJO, forma="circulo")

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)

# Variables globales
dificultad = "Seleccionando"
velocidad_enemigo = 2


def mostrar_texto(texto, x, y, fuente, color=BLANCO):
    t = fuente.render(texto, True, color)
    pantalla.blit(t, (x, y))


def boton(texto, x, y, w, h, color_base=(50, 50, 200), color_hover=AZUL):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    dentro = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = color_hover if dentro else color_base
    pygame.draw.rect(pantalla, color, (x, y, w, h))
    
    t = fuente.render(texto, True, BLANCO)
    t_rect = t.get_rect(center=(x + w // 2, y + h // 2))
    pantalla.blit(t, t_rect)
    
    if dentro and click[0]:
        pygame.time.wait(150)
        return True
    return False


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
    dificultad = "Seleccionando"
    while dificultad == "Seleccionando":
        pantalla.fill(NEGRO)
        mostrar_texto("Selecciona dificultad", 160, 100, fuente_grande)

        if boton("Fácil", 300, 200, 200, 50):
            set_dificultad("Fácil")
        if boton("Normal", 300, 270, 200, 50):
            set_dificultad("Normal")
        if boton("Difícil", 300, 340, 200, 50):
            set_dificultad("Difícil")
        if boton("Extremo", 300, 410, 200, 50):
            set_dificultad("Extremo")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(30)


def juego():
    jugador_x = 376
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
            mostrar_texto("GAME OVER", 240, 200, fuente_grande, ROJO)
            mostrar_texto(f"Puntaje final: {puntaje}", 290, 280, fuente)
            
            if boton("Reintentar", 300, 360, 200, 50):
                return True

        pygame.display.update()

    return False


def main():
    while True:
        seleccionar_dificultad()
        reiniciar = juego()
        if not reiniciar:
            break


if __name__ == "__main__":
    main()
