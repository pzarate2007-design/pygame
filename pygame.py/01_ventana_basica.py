"""
01_ventana_basica.py
Lo mínimo que necesita cualquier programa Pygame: iniciar, crear la ventana,
el "bucle del juego" (game loop), el control de FPS y la salida limpia.
"""
import pygame

pygame.init()  # 1) Inicia todos los módulos de Pygame

ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # 2) Crea la ventana
pygame.display.set_caption("01 - Ventana básica")

reloj = pygame.time.Clock()  # Sirve para controlar los FPS (cuadros por segundo)
corriendo = True

# 3) El bucle del juego: se repite ~60 veces por segundo
while corriendo:
    # a) Eventos: todo lo que hace el usuario (cerrar, teclas, mouse...)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # clic en la X de la ventana
            corriendo = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            corriendo = False

    # b) Dibujar: primero se rellena el fondo con un color (R, G, B)
    pantalla.fill((30, 30, 60))

    # c) Mostrar en pantalla lo que se dibujó
    pygame.display.flip()

    # d) Limitar a 60 FPS
    reloj.tick(60)

pygame.quit()  # 4) Cerrar Pygame correctamente
