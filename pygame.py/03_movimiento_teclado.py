"""
03_movimiento_teclado.py
Mover un objeto con el teclado (flechas o WASD) usando pygame.key.get_pressed()
y delta time para que la velocidad sea la misma en cualquier computadora.
"""
import pygame

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("03 - Movimiento con teclado")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 20)

jugador = pygame.Rect(300, 220, 50, 50)  # Rect = posición + tamaño
VELOCIDAD = 300  # píxeles por SEGUNDO

corriendo = True
while corriendo:
    # dt = segundos que pasaron desde el cuadro anterior
    dt = reloj.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # get_pressed() devuelve qué teclas están sostenidas AHORA
    teclas = pygame.key.get_pressed()
    dx = dy = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        dx -= 1
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        dx += 1
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        dy -= 1
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        dy += 1

    jugador.x += dx * VELOCIDAD * dt
    jugador.y += dy * VELOCIDAD * dt

    # clamp_ip evita que el rectángulo salga de la pantalla
    jugador.clamp_ip(pantalla.get_rect())

    pantalla.fill((25, 25, 40))
    pygame.draw.rect(pantalla, (80, 200, 255), jugador, border_radius=8)
    pantalla.blit(
        fuente.render("Flechas o WASD para moverte", True, (200, 200, 200)), (10, 10)
    )
    pantalla.blit(
        fuente.render(f"Posición: {jugador.x}, {jugador.y}", True, (200, 200, 200)), (10, 36)
    )
    pygame.display.flip()

pygame.quit()
