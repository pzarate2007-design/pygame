"""
05_colisiones.py
Detectar colisiones con Rect.colliderect() y colliderect con listas.
Mueve el cuadro azul con las flechas: los obstáculos rojos cambian de color al tocarlos
y las monedas amarillas desaparecen y suman puntos.
"""
import random
import pygame

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("05 - Colisiones")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 22)

jugador = pygame.Rect(40, 200, 40, 40)
obstaculos = [pygame.Rect(200, 100, 100, 60), pygame.Rect(380, 280, 80, 120), pygame.Rect(120, 330, 140, 40)]
monedas = [pygame.Rect(random.randint(20, ANCHO - 40), random.randint(20, ALTO - 40), 20, 20) for _ in range(8)]
puntos = 0
VELOCIDAD = 280

corriendo = True
while corriendo:
    dt = reloj.tick(60) / 1000
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    anterior = jugador.copy()  # guardamos la posición por si hay que regresar
    jugador.x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * VELOCIDAD * dt
    jugador.y += (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * VELOCIDAD * dt
    jugador.clamp_ip(pantalla.get_rect())

    # colliderect: ¿se tocan dos rectángulos?
    tocando = False
    for obstaculo in obstaculos:
        if jugador.colliderect(obstaculo):
            tocando = True
            jugador = anterior  # lo regresamos: los obstáculos son "paredes"

    # collidelist: devuelve el índice de la primera colisión de una lista (o -1)
    indice = jugador.collidelist(monedas)
    if indice != -1:
        monedas.pop(indice)
        puntos += 10

    pantalla.fill((25, 25, 40))
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, (255, 120, 40) if tocando else (200, 50, 50), obstaculo)
    for moneda in monedas:
        pygame.draw.ellipse(pantalla, (250, 220, 50), moneda)
    pygame.draw.rect(pantalla, (80, 200, 255), jugador, border_radius=6)

    pantalla.blit(fuente.render(f"Puntos: {puntos}", True, (255, 255, 255)), (10, 10))
    if not monedas:
        pantalla.blit(fuente.render("¡Recogiste todas las monedas!", True, (120, 255, 120)), (190, 220))

    pygame.display.flip()

pygame.quit()
