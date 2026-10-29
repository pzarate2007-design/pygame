"""
04_mouse_y_eventos.py
Eventos del mouse y del teclado:
- Clic izquierdo: crea un círculo de color aleatorio
- Clic derecho: borra todos
- Rueda del mouse: cambia el tamaño
- Barra espaciadora: cambia el color de fondo
- Un círculo blanco siempre sigue al cursor
"""
import random
import pygame

pygame.init()
pantalla = pygame.display.set_mode((640, 480))
pygame.display.set_caption("04 - Mouse y eventos")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 18)

circulos = []  # lista de (posición, radio, color)
radio = 20
fondo = (25, 25, 40)

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # izquierdo
                color = (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))
                circulos.append((evento.pos, radio, color))
            elif evento.button == 3:  # derecho
                circulos.clear()

        elif evento.type == pygame.MOUSEWHEEL:
            radio = max(5, min(80, radio + evento.y * 3))

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                fondo = (random.randint(0, 60), random.randint(0, 60), random.randint(0, 60))

    pantalla.fill(fondo)
    for pos, r, color in circulos:
        pygame.draw.circle(pantalla, color, pos, r)

    # Posición actual del cursor
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(pantalla, (255, 255, 255), (mx, my), radio, 2)

    ayuda = [
        "Clic izquierdo: crear círculo",
        "Clic derecho: borrar todo",
        "Rueda del mouse: cambiar tamaño",
        "Espacio: cambiar fondo",
        f"Círculos: {len(circulos)}   Radio: {radio}",
    ]
    for i, linea in enumerate(ayuda):
        pantalla.blit(fuente.render(linea, True, (220, 220, 220)), (10, 10 + i * 22))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
