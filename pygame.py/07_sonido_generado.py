"""
07_sonido_generado.py
Sonido con pygame.mixer SIN necesitar archivos de audio: se generan tonos con matemáticas.
Teclas 1 a 8: notas Do a Do agudo. Barra espaciadora: efecto "láser".
Si tu computadora no tiene salida de audio, el programa te avisa y sigue funcionando.
"""
import array
import math
import pygame

FRECUENCIA_MUESTREO = 44100

pygame.mixer.pre_init(FRECUENCIA_MUESTREO, -16, 1, 512)
pygame.init()
pantalla = pygame.display.set_mode((640, 300))
pygame.display.set_caption("07 - Sonido generado")
fuente = pygame.font.SysFont("arial", 22)


def crear_tono(frecuencia, duracion=0.4, volumen=0.4, bajada=False):
    """Genera una onda senoidal y la convierte en un objeto Sound."""
    total = int(FRECUENCIA_MUESTREO * duracion)
    muestras = array.array("h")
    for i in range(total):
        f = frecuencia * (1 - 0.7 * i / total) if bajada else frecuencia  # "bajada" = láser
        envolvente = 1 - i / total  # el sonido se va apagando
        valor = math.sin(2 * math.pi * f * i / FRECUENCIA_MUESTREO) * envolvente
        muestras.append(int(valor * volumen * 32767))
    return pygame.mixer.Sound(buffer=muestras.tobytes())


try:
    notas = [261.6, 293.7, 329.6, 349.2, 392.0, 440.0, 493.9, 523.3]
    sonidos = {pygame.K_1 + i: crear_tono(f) for i, f in enumerate(notas)}
    laser = crear_tono(1200, 0.25, 0.3, bajada=True)
    audio_ok = True
except pygame.error as error:
    print("No se pudo iniciar el audio:", error)
    audio_ok = False

ultima = "Presiona 1-8 o ESPACIO"
reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN and audio_ok:
            if evento.key in sonidos:
                sonidos[evento.key].play()
                ultima = f"Nota {evento.key - pygame.K_0}"
            elif evento.key == pygame.K_SPACE:
                laser.play()
                ultima = "¡Láser!"

    pantalla.fill((25, 25, 40))
    mensaje = ultima if audio_ok else "Sin audio disponible"
    pantalla.blit(fuente.render("Teclas 1-8: notas | Espacio: láser", True, (200, 200, 200)), (20, 30))
    pantalla.blit(fuente.render(mensaje, True, (120, 255, 160)), (20, 120))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
