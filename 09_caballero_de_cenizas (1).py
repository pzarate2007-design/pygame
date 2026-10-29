"""
09_caballero_de_cenizas.py
JUEGO "souls-like" (inspirado en Elden Ring) · vista desde arriba

Un combate contra jefe donde importa más la paciencia que los botones:
aprende los ataques del Gran Centinela Calcinado, esquiva con la voltereta
y golpea cuando termine de atacar. Cuida tu resistencia (barra verde).

CONTROLES
  WASD ................ moverte
  Ratón ............... apuntar (hacia dónde miras)
  Clic izquierdo / J .. atacar (gasta resistencia)
  ESPACIO ............. voltereta (invulnerable un instante, gasta resistencia)
  Q ................... beber un frasco de curación (3 por partida)
  ENTER ............... reintentar al terminar          ESC: salir

CONCEPTOS DE PYGAME QUE USA
  Vector2, máquina de estados del jefe, hitboxes con ángulo, ataques con
  aviso (telegraph), invulnerabilidad temporal, partículas y sacudida de pantalla.
"""
import math
import random
import pygame

pygame.init()
ANCHO, ALTO = 960, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Caballero de Cenizas")
reloj = pygame.time.Clock()
V = pygame.Vector2

ARENA = pygame.Rect(50, 50, ANCHO - 100, ALTO - 140)
LIENZO = pygame.Surface((ANCHO, ALTO))                 # aquí se dibuja el mundo
CAPA = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)  # efectos translúcidos

F_PEQ = pygame.font.SysFont("georgia", 16)
F_MED = pygame.font.SysFont("georgia", 26)
F_GRANDE = pygame.font.SysFont("georgia", 76, bold=True)


def escribir(sup, txt, fuente, color, centro=None, izq=None, alfa=255):
    img = fuente.render(txt, True, color)
    img.set_alpha(alfa)
    rect = img.get_rect()
    if centro:
        rect.center = centro
    elif izq:
        rect.topleft = izq
    sup.blit(img, rect)


def sector(centro, direccion, radio, apertura, color):
    """Dibuja en CAPA un 'gajo' de círculo (sirve para el tajo de la espada)."""
    base = math.atan2(direccion.y, direccion.x)
    puntos = [(centro.x, centro.y)]
    for i in range(13):
        a = base - apertura / 2 + apertura * i / 12
        puntos.append((centro.x + radio * math.cos(a), centro.y + radio * math.sin(a)))
    pygame.draw.polygon(CAPA, color, puntos)


def disco(centro, radio, color):
    pygame.draw.circle(CAPA, color, (int(centro.x), int(centro.y)), int(radio))


# ------------------------------------------------------------- JUGADOR ----
class Jugador:
    RADIO = 16

    def __init__(self):
        self.pos = V(ANCHO / 2, ARENA.bottom - 70)
        self.vida_max = 100
        self.vida = 100
        self.stam_max = 100
        self.stam = 100.0
        self.pausa_stam = 0.0   # tiempo antes de recuperar resistencia
        self.frascos = 3
        self.dir = V(0, -1)
        self.mover = V(0, 0)
        self.rodar_t = 0.0
        self.rodar_dir = V(0, -1)
        self.atacar_t = 0.0
        self.golpe_dado = False
        self.beber_t = 0.0
        self.inv_golpe = 0.0

    @property
    def invulnerable(self):
        # La voltereta protege solo en la parte central (como en los souls-like)
        return (0.06 < self.rodar_t < 0.32) or self.inv_golpe > 0

    def atacar(self):
        if self.atacar_t <= 0 and self.rodar_t <= 0 and self.stam >= 18:
            self.atacar_t = 0.35
            self.stam -= 18
            self.pausa_stam = 0.7
            self.golpe_dado = False

    def rodar(self):
        if self.rodar_t <= 0 and self.atacar_t <= 0 and self.stam >= 22:
            self.rodar_t = 0.38
            self.rodar_dir = V(self.mover) if self.mover.length() > 0 else V(self.dir)
            self.stam -= 22
            self.pausa_stam = 0.5

    def beber(self):
        if self.frascos > 0 and self.vida < self.vida_max and self.beber_t <= 0 and self.rodar_t <= 0:
            self.frascos -= 1
            self.vida = min(self.vida_max, self.vida + 45)
            self.beber_t = 0.7

    def recibir(self, dano, juego):
        if self.invulnerable:
            return
        self.vida -= dano
        self.inv_golpe = 0.7
        juego.sacudida = 0.25
        juego.chispas(self.pos, (200, 40, 40), 12)

    def actualizar(self, dt, teclas, raton):
        self.mover = V(teclas[pygame.K_d] - teclas[pygame.K_a], teclas[pygame.K_s] - teclas[pygame.K_w])
        if self.mover.length() > 0:
            self.mover = self.mover.normalize()
        if self.rodar_t <= 0:
            apuntar = V(raton) - self.pos
            if apuntar.length() > 4:
                self.dir = apuntar.normalize()

        if self.rodar_t > 0:
            self.pos += self.rodar_dir * 520 * dt
        else:
            vel = 215
            if self.atacar_t > 0:
                vel *= 0.45
            if self.beber_t > 0:
                vel *= 0.4
            self.pos += self.mover * vel * dt

        self.pos.x = max(ARENA.left + self.RADIO, min(ARENA.right - self.RADIO, self.pos.x))
        self.pos.y = max(ARENA.top + self.RADIO, min(ARENA.bottom - self.RADIO, self.pos.y))

        for nombre in ("rodar_t", "atacar_t", "beber_t", "inv_golpe", "pausa_stam"):
            setattr(self, nombre, max(0.0, getattr(self, nombre) - dt))
        if self.pausa_stam <= 0 and self.rodar_t <= 0 and self.atacar_t <= 0:
            self.stam = min(self.stam_max, self.stam + 40 * dt)


# ---------------------------------------------------------------- JEFE ----
class Proyectil:
    def __init__(self, pos, vel):
        self.pos = V(pos)
        self.vel = V(vel)
        self.ttl = 4.0
        self.radio = 9

    def actualizar(self, dt):
        self.pos += self.vel * dt
        self.ttl -= dt


class Jefe:
    """Máquina de estados: espera -> (tajo | embestida | orbes) con fases aviso/golpe/recuperar."""

    def __init__(self):
        self.pos = V(ANCHO / 2, ARENA.top + 150)
        self.radio = 42
        self.vida_max = 420
        self.vida = 420
        self.estado = "espera"
        self.sub = ""
        self.t = 1.5
        self.t_aviso = 1.0
        self.dir = V(0, 1)
        self.golpeo = False
        self.destello = 0.0

    @property
    def fase2(self):
        return self.vida < self.vida_max * 0.5

    def elegir(self, jg):
        distancia = (jg.pos - self.pos).length()
        opciones = ["tajo"] * (3 if distancia < 200 else 1) + ["embestida"] * (2 if distancia >= 200 else 1)
        if self.fase2:
            opciones += ["orbes"] * 2
        self.estado = random.choice(opciones)
        self.sub = "aviso"
        base = {"tajo": 0.9, "embestida": 0.8, "orbes": 0.8}[self.estado]
        self.t_aviso = base / (1.3 if self.fase2 else 1.0)
        self.t = self.t_aviso
        self.golpeo = False
        a = jg.pos - self.pos
        self.dir = a.normalize() if a.length() > 0 else V(0, 1)

    def actualizar(self, dt, jg, juego):
        self.destello = max(0.0, self.destello - dt)
        self.t -= dt
        rapido = 1.3 if self.fase2 else 1.0

        if self.estado == "espera":
            a = jg.pos - self.pos
            if a.length() > 0:
                self.dir = a.normalize()
            if a.length() > 110:
                self.pos += self.dir * 80 * rapido * dt
            if self.t <= 0:
                self.elegir(jg)
            return

        if self.sub == "aviso":
            if self.estado == "embestida" and self.t > 0.3:  # sigue al jugador y luego se fija
                a = jg.pos - self.pos
                if a.length() > 0:
                    self.dir = a.normalize()
            if self.t <= 0:
                self.sub = "golpe"
                if self.estado == "tajo":
                    self.t = 0.15
                    juego.ondas.append([V(self.pos), 125, 0.3])
                    juego.sacudida = 0.3
                    if (jg.pos - self.pos).length() < 125 + jg.RADIO:
                        jg.recibir(32, juego)
                elif self.estado == "embestida":
                    self.t = 0.5
                else:  # orbes
                    self.t = 0.1
                    desfase = random.random()
                    for i in range(10):
                        ang = desfase + i * 2 * math.pi / 10
                        juego.proyectiles.append(Proyectil(self.pos, V(math.cos(ang), math.sin(ang)) * 250))

        elif self.sub == "golpe":
            if self.estado == "embestida":
                self.pos += self.dir * 650 * dt
                self.pos.x = max(ARENA.left + self.radio, min(ARENA.right - self.radio, self.pos.x))
                self.pos.y = max(ARENA.top + self.radio, min(ARENA.bottom - self.radio, self.pos.y))
                if not self.golpeo and (jg.pos - self.pos).length() < self.radio + jg.RADIO:
                    self.golpeo = True
                    jg.recibir(28, juego)
            if self.t <= 0:
                self.sub = "recuperar"
                self.t = (1.0 if self.estado == "tajo" else 0.85) / rapido

        elif self.sub == "recuperar":  # el jugador puede castigarlo aquí
            if self.t <= 0:
                self.estado = "espera"
                self.sub = ""
                self.t = random.uniform(0.6, 1.2)


# --------------------------------------------------------------- JUEGO ----
class Juego:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.j = Jugador()
        self.jefe = Jefe()
        self.proyectiles = []
        self.ondas = []
        self.particulas = []
        self.estado = "jugando"
        self.t_fin = 0.0
        self.sacudida = 0.0

    def chispas(self, pos, color, n):
        for _ in range(n):
            ang = random.uniform(0, 2 * math.pi)
            vel = random.uniform(60, 220)
            self.particulas.append([V(pos), V(math.cos(ang), math.sin(ang)) * vel, random.uniform(0.25, 0.6), color])

    # ---- lógica ----
    def actualizar(self, dt):
        self.sacudida = max(0.0, self.sacudida - dt)
        for p in self.particulas:
            p[0] += p[1] * dt
            p[2] -= dt
        self.particulas = [p for p in self.particulas if p[2] > 0]

        if self.estado != "jugando":
            self.t_fin += dt
            return

        j, jefe = self.j, self.jefe
        j.actualizar(dt, pygame.key.get_pressed(), pygame.mouse.get_pos())
        jefe.actualizar(dt, j, self)

        # Golpe del jugador: solo en la parte "activa" de la animación, dentro de un arco
        if 0.10 < j.atacar_t < 0.25 and not j.golpe_dado:
            v = jefe.pos - j.pos
            if 0 < v.length() < 85 + jefe.radio and j.dir.dot(v.normalize()) > math.cos(math.radians(65)):
                jefe.vida -= 14
                jefe.destello = 0.12
                j.golpe_dado = True
                self.chispas(jefe.pos - v.normalize() * jefe.radio, (255, 220, 120), 10)

        for p in self.proyectiles:
            p.actualizar(dt)
            if (p.pos - j.pos).length() < p.radio + j.RADIO:
                j.recibir(14, self)
                p.ttl = 0
        self.proyectiles = [p for p in self.proyectiles
                            if p.ttl > 0 and ARENA.inflate(60, 60).collidepoint(p.pos)]

        for onda in self.ondas:
            onda[2] -= dt
        self.ondas = [o for o in self.ondas if o[2] > 0]

        if j.vida <= 0:
            self.estado = "muerto"
        elif jefe.vida <= 0:
            self.estado = "victoria"
            self.chispas(jefe.pos, (255, 200, 80), 60)

    # ---- dibujo ----
    def dibujar_arena(self, S):
        S.fill((18, 15, 14))
        pygame.draw.rect(S, (44, 38, 34), ARENA)
        for x in range(ARENA.left, ARENA.right, 80):
            pygame.draw.line(S, (38, 33, 29), (x, ARENA.top), (x, ARENA.bottom))
        for y in range(ARENA.top, ARENA.bottom, 80):
            pygame.draw.line(S, (38, 33, 29), (ARENA.left, y), (ARENA.right, y))
        for radio in (210, 150, 70):
            pygame.draw.circle(S, (62, 52, 40), ARENA.center, radio, 3)
        pygame.draw.rect(S, (95, 78, 55), ARENA, 4)
        llama = 7 + int(2 * math.sin(pygame.time.get_ticks() / 120))
        for esquina in (ARENA.topleft, ARENA.topright, ARENA.bottomleft, ARENA.bottomright):
            pygame.draw.circle(S, (28, 24, 22), esquina, 30)
            pygame.draw.circle(S, (110, 90, 60), esquina, 30, 3)
            pygame.draw.circle(S, (255, 150, 40), esquina, llama + 2)

    def telegrafos(self):
        jefe = self.jefe
        if jefe.sub != "aviso":
            return
        p = 1 - max(0.0, jefe.t) / jefe.t_aviso  # progreso del aviso 0 -> 1
        if jefe.estado == "tajo":
            disco(jefe.pos, 125, (255, 60, 40, 45))
            disco(jefe.pos, 125 * p, (255, 60, 40, 110))
        elif jefe.estado == "embestida":
            n = V(-jefe.dir.y, jefe.dir.x) * jefe.radio
            fin = jefe.pos + jefe.dir * 700
            pygame.draw.polygon(CAPA, (255, 60, 40, 55), [jefe.pos + n, jefe.pos - n, fin - n, fin + n])
        else:
            disco(jefe.pos, 50 + 30 * p, (255, 170, 60, 90))

    def dibujar_jefe(self, S):
        jefe = self.jefe
        c = (255, 255, 255) if jefe.destello > 0 else (58, 40, 40)
        x, y = int(jefe.pos.x), int(jefe.pos.y)
        perp = V(-jefe.dir.y, jefe.dir.x)
        # espada enorme
        punta = jefe.pos + jefe.dir * 95
        pygame.draw.line(S, (120, 95, 80), jefe.pos + jefe.dir * 20, punta, 9)
        pygame.draw.line(S, (200, 180, 160), jefe.pos + jefe.dir * 20, punta, 3)
        # cuerpo, armadura y cuernos
        pygame.draw.circle(S, c, (x, y), jefe.radio)
        pygame.draw.circle(S, (110, 80, 60) if jefe.destello <= 0 else c, (x, y), jefe.radio, 5)
        for lado in (-1, 1):
            base = jefe.pos + perp * 26 * lado
            punta_c = jefe.pos + perp * 46 * lado - jefe.dir * 26
            pygame.draw.line(S, (200, 180, 150), base, punta_c, 6)
        for lado in (-1, 1):  # ojos que brillan
            ojo = jefe.pos + jefe.dir * 18 + perp * 11 * lado
            pygame.draw.circle(S, (255, 140, 40), (int(ojo.x), int(ojo.y)), 5)

    def dibujar_jugador(self, S):
        j = self.j
        if j.inv_golpe > 0 and int(j.inv_golpe * 20) % 2 == 0:
            return
        x, y = int(j.pos.x), int(j.pos.y)
        if j.rodar_t > 0:  # durante la voltereta se ve "encogido"
            pygame.draw.ellipse(S, (150, 160, 175), (x - 18, y - 11, 36, 22))
            return
        perp = V(-j.dir.y, j.dir.x)
        pygame.draw.circle(S, (160, 170, 185), (x, y), j.RADIO)
        pygame.draw.circle(S, (230, 235, 245), (x, y), j.RADIO, 3)
        pygame.draw.circle(S, (40, 45, 60), (int(x + j.dir.x * 7), int(y + j.dir.y * 7)), 5)  # visera
        mano = j.pos + perp * 12
        pygame.draw.line(S, (210, 215, 225), mano, mano + j.dir * 34, 4)
        if j.atacar_t > 0:
            progreso = 1 - j.atacar_t / 0.35
            sector(j.pos, j.dir, 85, math.radians(130), (255, 245, 200, int(170 * (1 - progreso * 0.6))))

    def dibujar_hud(self):
        j, jefe = self.j, self.jefe
        # Vida
        pygame.draw.rect(pantalla, (30, 10, 10), (20, 14, 322, 18))
        pygame.draw.rect(pantalla, (180, 30, 40), (21, 15, int(320 * max(0, j.vida) / j.vida_max), 16))
        pygame.draw.rect(pantalla, (120, 100, 70), (20, 14, 322, 18), 2)
        # Resistencia
        pygame.draw.rect(pantalla, (10, 30, 10), (20, 38, 242, 12))
        pygame.draw.rect(pantalla, (70, 190, 80), (21, 39, int(240 * j.stam / j.stam_max), 10))
        pygame.draw.rect(pantalla, (120, 100, 70), (20, 38, 242, 12), 2)
        escribir(pantalla, f"Frascos: {j.frascos}", F_PEQ, (230, 200, 120), izq=(280, 36))
        # Jefe (barra inferior)
        ancho = 600
        x0 = ANCHO // 2 - ancho // 2
        escribir(pantalla, "GRAN CENTINELA CALCINADO", F_PEQ, (230, 210, 170), centro=(ANCHO // 2, ALTO - 58))
        pygame.draw.rect(pantalla, (30, 10, 10), (x0, ALTO - 44, ancho, 14))
        pygame.draw.rect(pantalla, (170, 40, 40), (x0 + 1, ALTO - 43, int((ancho - 2) * max(0, jefe.vida) / jefe.vida_max), 12))
        pygame.draw.rect(pantalla, (120, 100, 70), (x0, ALTO - 44, ancho, 14), 2)
        escribir(pantalla, "WASD mover · Ratón apuntar · Clic/J atacar · ESPACIO voltereta · Q frasco",
                 F_PEQ, (150, 140, 120), centro=(ANCHO // 2, ALTO - 14))

    def dibujar(self):
        S = LIENZO
        self.dibujar_arena(S)
        CAPA.fill((0, 0, 0, 0))
        self.telegrafos()
        for pos, radio, t in self.ondas:  # anillo de la onda de choque
            pygame.draw.circle(CAPA, (255, 170, 70, int(220 * t / 0.3)), (int(pos.x), int(pos.y)), int(radio), 8)
        S.blit(CAPA, (0, 0))
        CAPA.fill((0, 0, 0, 0))

        self.dibujar_jefe(S)
        self.dibujar_jugador(S)
        for p in self.proyectiles:
            pygame.draw.circle(S, (255, 150, 50), (int(p.pos.x), int(p.pos.y)), p.radio)
            pygame.draw.circle(S, (255, 235, 160), (int(p.pos.x), int(p.pos.y)), p.radio - 4)
        for pos, _vel, ttl, color in self.particulas:
            pygame.draw.circle(S, color, (int(pos.x), int(pos.y)), max(1, int(ttl * 8)))
        S.blit(CAPA, (0, 0))  # el tajo se dibuja encima

        ox = oy = 0
        if self.sacudida > 0:
            ox = random.randint(-6, 6)
            oy = random.randint(-6, 6)
        pantalla.fill((0, 0, 0))
        pantalla.blit(S, (ox, oy))
        self.dibujar_hud()

        if self.estado == "muerto":
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((0, 0, 0, int(min(190, self.t_fin * 140))))
            pantalla.blit(velo, (0, 0))
            escribir(pantalla, "HAS CAÍDO", F_GRANDE, (170, 25, 30), centro=(ANCHO // 2, ALTO // 2),
                     alfa=int(min(255, self.t_fin * 200)))
            if self.t_fin > 1.5:
                escribir(pantalla, "ENTER para reintentar", F_MED, (220, 220, 220), centro=(ANCHO // 2, ALTO // 2 + 80))
        elif self.estado == "victoria":
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((0, 0, 0, int(min(120, self.t_fin * 100))))
            pantalla.blit(velo, (0, 0))
            escribir(pantalla, "ENEMIGO ABATIDO", F_GRANDE, (235, 200, 90), centro=(ANCHO // 2, ALTO // 2),
                     alfa=int(min(255, self.t_fin * 200)))
            if self.t_fin > 1.5:
                escribir(pantalla, "ENTER para jugar de nuevo", F_MED, (220, 220, 220), centro=(ANCHO // 2, ALTO // 2 + 80))

    def ejecutar(self):
        corriendo = True
        while corriendo:
            dt = min(reloj.tick(60) / 1000, 0.05)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    corriendo = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        corriendo = False
                    elif self.estado == "jugando":
                        if e.key == pygame.K_SPACE:
                            self.j.rodar()
                        elif e.key == pygame.K_j:
                            self.j.atacar()
                        elif e.key == pygame.K_q:
                            self.j.beber()
                    elif e.key == pygame.K_RETURN and self.t_fin > 1.0:
                        self.reiniciar()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.estado == "jugando":
                    self.j.atacar()
            self.actualizar(dt)
            self.dibujar()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Juego().ejecutar()
