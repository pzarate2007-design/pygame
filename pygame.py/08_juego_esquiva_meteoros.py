"""
08_juego_esquiva_meteoros.py
VIDEOJUEGO: "Esquiva Meteoros"

Pilota una nave espacial, esquiva (o destruye) los meteoros y atrapa estrellas.
Todo se dibuja con código: no necesita imágenes ni sonidos externos.

CONTROLES
  Flechas o WASD ... mover la nave
  ESPACIO ........... disparar (mantenlo presionado)
  ENTER ............. empezar / jugar de nuevo
  P ................. pausa
  ESC ............... salir

REGLAS
  - Tienes 3 vidas. Cada choque con un meteoro te quita una.
  - Disparar a un meteoro: +5 puntos.  Atrapar una estrella: +20 puntos y,
    si te faltan vidas, recuperas una cada 3 estrellas.
  - Cada 15 segundos sube el nivel: caen más meteoros y más rápido.
"""
import math
import random
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
FPS = 60
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva Meteoros")

# Estados del juego
MENU, JUGANDO, PAUSA, FIN = "menu", "jugando", "pausa", "fin"

FUENTE_TITULO = pygame.font.SysFont("arial", 64, bold=True)
FUENTE_GRANDE = pygame.font.SysFont("arial", 36, bold=True)
FUENTE = pygame.font.SysFont("arial", 24)
FUENTE_CHICA = pygame.font.SysFont("arial", 18)


def escribir(texto, fuente, color, centro=None, arriba_izq=None, derecha=None):
    """Dibuja texto en pantalla. Se puede colocar por centro, esquina o borde derecho."""
    imagen = fuente.render(texto, True, color)
    rect = imagen.get_rect()
    if centro:
        rect.center = centro
    elif arriba_izq:
        rect.topleft = arriba_izq
    elif derecha:
        rect.topright = derecha
    pantalla.blit(imagen, rect)


# ---------------------------------------------------------------- SPRITES ----
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((46, 54), pygame.SRCALPHA)
        forma = [(23, 0), (46, 50), (23, 40), (0, 50)]
        pygame.draw.polygon(self.image, (90, 200, 255), forma)
        pygame.draw.polygon(self.image, (255, 255, 255), forma, 2)
        pygame.draw.circle(self.image, (255, 255, 255), (23, 26), 5)
        self.rect = self.image.get_rect()
        self.radius = 18  # lo usa collide_circle para colisiones más justas
        self.velocidad = 340
        self.reiniciar()

    def reiniciar(self):
        self.pos = pygame.Vector2(ANCHO / 2, ALTO - 80)
        self.rect.center = self.pos
        self.invulnerable = 0.0

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        direccion = pygame.Vector2(
            (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a]),
            (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w]),
        )
        if direccion.length() > 0:
            direccion = direccion.normalize()  # misma velocidad en diagonal
        self.pos += direccion * self.velocidad * dt
        self.pos.x = max(25, min(ANCHO - 25, self.pos.x))
        self.pos.y = max(ALTO // 2, min(ALTO - 30, self.pos.y))  # solo mitad inferior
        self.rect.center = self.pos

        # Tras un golpe la nave parpadea y no puede ser dañada por un momento
        if self.invulnerable > 0:
            self.invulnerable -= dt
            self.image.set_alpha(90 if (pygame.time.get_ticks() // 100) % 2 else 255)
        else:
            self.image.set_alpha(255)


class Meteoro(pygame.sprite.Sprite):
    def __init__(self, nivel):
        super().__init__()
        self.radius = random.randint(15, 38)
        d = self.radius * 2
        self.image = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (135, 115, 105), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (90, 75, 70), (self.radius, self.radius), self.radius, 3)
        for _ in range(3):  # cráteres
            r = random.randint(3, max(4, self.radius // 4))
            cx = random.randint(self.radius // 2, d - self.radius // 2)
            cy = random.randint(self.radius // 2, d - self.radius // 2)
            pygame.draw.circle(self.image, (95, 80, 75), (cx, cy), r)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(random.randint(self.radius, ANCHO - self.radius), -d)
        velocidad = random.randint(120, 200) + 25 * nivel
        self.vel = pygame.Vector2(random.uniform(-60, 60), velocidad)
        self.rect.center = self.pos

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if self.rect.top > ALTO or self.rect.right < -50 or self.rect.left > ANCHO + 50:
            self.kill()


class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        puntos = []
        for i in range(10):  # estrella de 5 puntas: radio exterior e interior alternados
            angulo = -math.pi / 2 + i * math.pi / 5
            radio = 14 if i % 2 == 0 else 6
            puntos.append((15 + radio * math.cos(angulo), 15 + radio * math.sin(angulo)))
        pygame.draw.polygon(self.image, (255, 225, 60), puntos)
        pygame.draw.polygon(self.image, (255, 255, 255), puntos, 1)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(random.randint(30, ANCHO - 30), -20)
        self.rect.center = self.pos

    def update(self, dt):
        self.pos.y += 140 * dt
        self.rect.center = self.pos
        if self.rect.top > ALTO:
            self.kill()


class Bala(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.Surface((6, 18), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 240, 120), (0, 0, 6, 18), border_radius=3)
        self.rect = self.image.get_rect(midbottom=posicion)
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        self.pos.y -= 620 * dt
        self.rect.center = self.pos
        if self.rect.bottom < 0:
            self.kill()


# ------------------------------------------------------------------ JUEGO ----
class Juego:
    def __init__(self):
        self.reloj = pygame.time.Clock()
        self.estado = MENU
        self.record = 0
        # Fondo de estrellitas con 3 capas de velocidad (efecto de profundidad)
        self.fondo = [
            [random.randint(0, ANCHO), random.randint(0, ALTO), random.choice((30, 70, 120))]
            for _ in range(90)
        ]
        self.jugador = Jugador()
        self.reiniciar()

    def reiniciar(self):
        """Deja todo listo para una partida nueva."""
        self.todos = pygame.sprite.Group()
        self.meteoros = pygame.sprite.Group()
        self.estrellas = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.jugador.reiniciar()
        self.todos.add(self.jugador)
        self.vidas = 3
        self.bonus = 0
        self.estrellas_atrapadas = 0
        self.tiempo = 0.0
        self.nivel = 1
        self.t_meteoro = 0.0
        self.t_estrella = 0.0
        self.prox_estrella = random.uniform(5, 9)
        self.enfriamiento = 0.0
        self.nuevo_record = False

    @property
    def puntaje(self):
        return self.bonus + int(self.tiempo * 2)  # 2 puntos por segundo sobrevivido

    # ---- lógica ----
    def actualizar(self, dt):
        self.tiempo += dt
        self.nivel = 1 + int(self.tiempo // 15)

        # Disparo (mantener ESPACIO)
        self.enfriamiento -= dt
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.enfriamiento <= 0:
            bala = Bala(self.jugador.rect.midtop)
            self.balas.add(bala)
            self.todos.add(bala)
            self.enfriamiento = 0.25

        # Aparición de meteoros: cada vez más seguido
        self.t_meteoro += dt
        if self.t_meteoro >= max(0.25, 0.85 - 0.06 * self.nivel):
            self.t_meteoro = 0
            meteoro = Meteoro(self.nivel)
            self.meteoros.add(meteoro)
            self.todos.add(meteoro)

        # Aparición de estrellas
        self.t_estrella += dt
        if self.t_estrella >= self.prox_estrella:
            self.t_estrella = 0
            self.prox_estrella = random.uniform(5, 9)
            estrella = Estrella()
            self.estrellas.add(estrella)
            self.todos.add(estrella)

        self.todos.update(dt)

        # Balas contra meteoros (ambos se destruyen)
        destruidos = pygame.sprite.groupcollide(self.balas, self.meteoros, True, True)
        for lista in destruidos.values():
            self.bonus += 5 * len(lista)

        # Jugador contra estrellas
        for _ in pygame.sprite.spritecollide(self.jugador, self.estrellas, True):
            self.bonus += 20
            self.estrellas_atrapadas += 1
            if self.estrellas_atrapadas % 3 == 0 and self.vidas < 3:
                self.vidas += 1

        # Jugador contra meteoros (collide_circle usa el atributo "radius")
        if self.jugador.invulnerable <= 0:
            golpes = pygame.sprite.spritecollide(
                self.jugador, self.meteoros, True, pygame.sprite.collide_circle
            )
            if golpes:
                self.vidas -= 1
                self.jugador.invulnerable = 1.5
                if self.vidas <= 0:
                    self.terminar()

    def terminar(self):
        self.estado = FIN
        if self.puntaje > self.record:
            self.record = self.puntaje
            self.nuevo_record = True

    # ---- dibujo ----
    def dibujar_fondo(self, dt):
        pantalla.fill((10, 10, 28))
        for estrella in self.fondo:
            estrella[1] += estrella[2] * dt
            if estrella[1] > ALTO:
                estrella[0], estrella[1] = random.randint(0, ANCHO), 0
            brillo = 100 + estrella[2]
            pygame.draw.circle(pantalla, (brillo, brillo, brillo), (int(estrella[0]), int(estrella[1])), 1 + estrella[2] // 60)

    def dibujar_hud(self):
        escribir(f"Puntos: {self.puntaje}", FUENTE, (255, 255, 255), arriba_izq=(15, 10))
        escribir(f"Nivel {self.nivel}", FUENTE, (255, 220, 120), arriba_izq=(15, 40))
        for i in range(self.vidas):  # un corazoncito por vida
            pygame.draw.circle(pantalla, (240, 70, 90), (ANCHO - 30 - i * 32, 25), 10)
        escribir(f"Récord: {self.record}", FUENTE_CHICA, (180, 180, 200), derecha=(ANCHO - 15, 48))

    def velo(self, alfa=150):
        capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        capa.fill((0, 0, 0, alfa))
        pantalla.blit(capa, (0, 0))

    def dibujar(self, dt):
        self.dibujar_fondo(dt)

        if self.estado == MENU:
            escribir("ESQUIVA METEOROS", FUENTE_TITULO, (120, 210, 255), centro=(ANCHO // 2, 150))
            instrucciones = [
                "Flechas / WASD: mover la nave",
                "ESPACIO: disparar",
                "P: pausa      ESC: salir",
                "Atrapa estrellas y evita los meteoros",
            ]
            for i, linea in enumerate(instrucciones):
                escribir(linea, FUENTE, (220, 220, 230), centro=(ANCHO // 2, 270 + i * 36))
            if (pygame.time.get_ticks() // 500) % 2:
                escribir("Presiona ENTER para jugar", FUENTE_GRANDE, (255, 230, 120), centro=(ANCHO // 2, 490))
            return

        self.todos.draw(pantalla)
        self.dibujar_hud()

        if self.estado == PAUSA:
            self.velo()
            escribir("PAUSA", FUENTE_TITULO, (255, 255, 255), centro=(ANCHO // 2, ALTO // 2 - 20))
            escribir("Presiona P para continuar", FUENTE, (220, 220, 220), centro=(ANCHO // 2, ALTO // 2 + 40))

        elif self.estado == FIN:
            self.velo(170)
            escribir("GAME OVER", FUENTE_TITULO, (255, 90, 100), centro=(ANCHO // 2, 190))
            escribir(f"Puntaje: {self.puntaje}", FUENTE_GRANDE, (255, 255, 255), centro=(ANCHO // 2, 280))
            if self.nuevo_record:
                escribir("¡NUEVO RÉCORD!", FUENTE_GRANDE, (255, 225, 60), centro=(ANCHO // 2, 335))
            else:
                escribir(f"Récord: {self.record}", FUENTE, (200, 200, 220), centro=(ANCHO // 2, 335))
            escribir("ENTER: jugar de nuevo      ESC: salir", FUENTE, (220, 220, 220), centro=(ANCHO // 2, 430))

    # ---- bucle principal ----
    def ejecutar(self):
        corriendo = True
        while corriendo:
            # min(...) evita saltos enormes si la ventana se congela un momento
            dt = min(self.reloj.tick(FPS) / 1000, 0.05)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        corriendo = False
                    elif evento.key == pygame.K_RETURN and self.estado in (MENU, FIN):
                        self.reiniciar()
                        self.estado = JUGANDO
                    elif evento.key == pygame.K_p:
                        if self.estado == JUGANDO:
                            self.estado = PAUSA
                        elif self.estado == PAUSA:
                            self.estado = JUGANDO

            if self.estado == JUGANDO:
                self.actualizar(dt)

            self.dibujar(dt)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Juego().ejecutar()
