"""
02_dibujo_formas.py
Dibujar figuras y texto: rectángulos, círculos, líneas, polígonos, elipses y fuentes.
"""
import pygame

pygame.init()
pantalla = pygame.display.set_mode((640, 480))
pygame.display.set_caption("02 - Dibujo de formas")
reloj = pygame.time.Clock()

# Colores como tuplas (rojo, verde, azul), cada valor de 0 a 255
BLANCO = (255, 255, 255)
ROJO = (220, 50, 50)
VERDE = (50, 200, 90)
AZUL = (60, 100, 230)
AMARILLO = (250, 220, 50)
NARANJA = (255, 150, 30)

fuente = pygame.font.SysFont("arial", 22)  # fuente del sistema
fuente_grande = pygame.font.SysFont("arial", 36, bold=True)

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((20, 20, 30))

    # Rectángulo: (x, y, ancho, alto). El último valor es el grosor (0 = relleno)
    pygame.draw.rect(pantalla, ROJO, (30, 60, 140, 80))
    pygame.draw.rect(pantalla, BLANCO, (30, 60, 140, 80), 3)

    # Rectángulo con esquinas redondeadas
    pygame.draw.rect(pantalla, VERDE, (200, 60, 140, 80), border_radius=20)

    # Círculo: (superficie, color, centro, radio)
    pygame.draw.circle(pantalla, AZUL, (440, 100), 45)
    pygame.draw.circle(pantalla, BLANCO, (440, 100), 45, 3)

    # Elipse: dentro de un rectángulo
    pygame.draw.ellipse(pantalla, AMARILLO, (520, 60, 100, 80))

    # Líneas
    pygame.draw.line(pantalla, BLANCO, (30, 200), (300, 260), 4)
    pygame.draw.lines(pantalla, NARANJA, False, [(330, 200), (380, 260), (430, 200), (480, 260)], 4)

    # Polígono (triángulo y estrella simple)
    pygame.draw.polygon(pantalla, ROJO, [(80, 330), (30, 420), (130, 420)])
    pygame.draw.polygon(
        pantalla, AMARILLO,
        [(250, 320), (270, 370), (325, 370), (280, 400), (298, 455),
         (250, 420), (202, 455), (220, 400), (175, 370), (230, 370)],
    )

    # Arco
    pygame.draw.arc(pantalla, VERDE, (380, 320, 120, 120), 0.5, 3.0, 5)

    # Texto: se crea una superficie con el texto y se "pega" con blit()
    texto = fuente_grande.render("¡Hola Pygame!", True, BLANCO)
    pantalla.blit(texto, (400, 400))
    pantalla.blit(fuente.render("Figuras y texto", True, (180, 180, 180)), (10, 10))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
