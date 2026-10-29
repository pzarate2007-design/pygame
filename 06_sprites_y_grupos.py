"""
06_sprites_y_grupos.py
Programación orientada a objetos con Pygame: clases Sprite y Group.
Caen "gotas" desde arriba; tú controlas un recipiente y las atrapas.
No usa imágenes externas: los sprites se dibujan con código.
"""
import random
import pygame

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("06 - Sprites y grupos")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 22)


class Recipiente(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image = lo que se dibuja; rect = dónde está
        self.image = pygame.Surface((90, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200, 160, 80), (0, 0, 90, 30), border_radius=8)
        self.rect = self.image.get_rect(midbottom=(ANCHO // 2, ALTO - 10))
        self.velocidad = 400

    def update(self, dt):  # se llama automáticamente desde grupo.update()
        teclas = pygame.key.get_pressed()
        self.rect.x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * self.velocidad * dt
        self.rect.clamp_ip(pantalla.get_rect())


class Gota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 22), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (80, 160, 255), (0, 0, 16, 22))
        self.rect = self.image.get_rect(midtop=(random.randint(20, ANCHO - 20), -20))
        self.velocidad = random.randint(150, 320)

    def update(self, dt):
        self.rect.y += self.velocidad * dt
        if self.rect.top > ALTO:
            self.kill()  # se elimina de todos los grupos


recipiente = Recipiente()
todos = pygame.sprite.Group(recipiente)  # grupo para dibujar y actualizar
gotas = pygame.sprite.Group()  # grupo solo para las gotas (para colisiones)

atrapadas = 0
perdidas = 0
EVENTO_GOTA = pygame.USEREVENT + 1  # evento propio
pygame.time.set_timer(EVENTO_GOTA, 500)  # cada 500 ms

corriendo = True
while corriendo:
    dt = reloj.tick(60) / 1000
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == EVENTO_GOTA:
            nueva = Gota()
            gotas.add(nueva)
            todos.add(nueva)

    antes = len(gotas)
    todos.update(dt)
    perdidas += antes - len(gotas)  # las que se salieron de la pantalla

    # spritecollide: sprites del grupo que tocan al recipiente (True = borrarlos).
    # Como se borran por colisión, no cuentan como "perdidas".
    for _ in pygame.sprite.spritecollide(recipiente, gotas, True):
        atrapadas += 1

    pantalla.fill((20, 30, 50))
    todos.draw(pantalla)
    pantalla.blit(fuente.render(f"Atrapadas: {atrapadas}   Perdidas: {perdidas}", True, (255, 255, 255)), (10, 10))
    pygame.display.flip()

pygame.quit()
