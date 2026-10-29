# 🎮 Pygame Demos: aprende a crear videojuegos con Python

Colección de **7 programas de ejemplo** que muestran las funcionalidades principales de **Pygame**, más **un videojuego completo** hecho con la librería: **Esquiva Meteoros**.

Los ejemplos van de menor a mayor dificultad y están comentados línea por línea. **No necesitan imágenes ni archivos de sonido externos**: todo se dibuja y se genera con código, así que basta con descargar el repositorio y ejecutar.

---

## 📋 Requisitos

- **Python 3.9 o superior** ([descargar](https://www.python.org/downloads/)).
- **Pygame** (no viene incluido con Python, hay que instalarlo).

### Instalación

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install pygame
```

o, usando el archivo de requisitos:

```bash
pip install -r requirements.txt
```

Comprueba que quedó instalado:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

> **Si `pip install pygame` falla** (puede pasar con versiones de Python muy recientes que aún no tienen paquete precompilado), prueba con **`pip install pygame-ce`**, que es una versión mantenida por la comunidad y se importa exactamente igual (`import pygame`). Otra opción es instalar Python 3.12 o 3.13.
>
> En Windows, si `python` no funciona, usa `py`. En macOS/Linux usa `python3` y `pip3`.

## ▶️ Cómo ejecutar

```bash
python 01_ventana_basica.py
```

Cambia el nombre por el archivo que quieras probar. Para el videojuego:

```bash
python 08_juego_esquiva_meteoros.py
```

En Visual Studio Code también puedes abrir el archivo y presionar el botón **▶** de arriba a la derecha.

---

## 📁 Estructura del repositorio

```
pygame-demos/
├── 01_ventana_basica.py
├── 02_dibujo_formas.py
├── 03_movimiento_teclado.py
├── 04_mouse_y_eventos.py
├── 05_colisiones.py
├── 06_sprites_y_grupos.py
├── 07_sonido_generado.py
├── 08_juego_esquiva_meteoros.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 📚 Resumen rápido

| Archivo | Tema | Nivel |
|---|---|---|
| [`01_ventana_basica.py`](01_ventana_basica.py) | Ventana, game loop, FPS | ⭐ |
| [`02_dibujo_formas.py`](02_dibujo_formas.py) | Figuras, colores y texto | ⭐ |
| [`03_movimiento_teclado.py`](03_movimiento_teclado.py) | Teclado, `Rect`, delta time | ⭐⭐ |
| [`04_mouse_y_eventos.py`](04_mouse_y_eventos.py) | Mouse, rueda, eventos | ⭐⭐ |
| [`05_colisiones.py`](05_colisiones.py) | Colisiones con `Rect` | ⭐⭐ |
| [`06_sprites_y_grupos.py`](06_sprites_y_grupos.py) | Clases `Sprite`, grupos, temporizadores | ⭐⭐⭐ |
| [`07_sonido_generado.py`](07_sonido_generado.py) | `mixer`, sonidos creados con código | ⭐⭐⭐ |
| [`08_juego_esquiva_meteoros.py`](08_juego_esquiva_meteoros.py) | **Videojuego completo** | ⭐⭐⭐⭐ |

---

## 🔎 Detalle de cada archivo

### [`01_ventana_basica.py`](01_ventana_basica.py)
**Qué hace:** abre una ventana con fondo de color y la mantiene abierta hasta que la cierres (X o tecla `ESC`).

**Conceptos que enseña:**
- `pygame.init()` y `pygame.quit()`: iniciar y cerrar Pygame.
- `pygame.display.set_mode()`: crear la ventana.
- **El bucle del juego (game loop)**: eventos → actualizar → dibujar → mostrar.
- `pygame.event.get()`: leer lo que hace el usuario.
- `fill()` y `display.flip()`: pintar el fondo y mostrar el cuadro terminado.
- `Clock.tick(60)`: limitar a 60 FPS.

---

### [`02_dibujo_formas.py`](02_dibujo_formas.py)
**Qué hace:** dibuja en pantalla rectángulos, círculos, elipses, líneas, polígonos, un arco y texto.

**Conceptos que enseña:**
- Colores en formato RGB `(rojo, verde, azul)`.
- `pygame.draw.rect`, `circle`, `ellipse`, `line`, `lines`, `polygon` y `arc`.
- Grosor de línea y relleno (grosor `0` = relleno).
- Esquinas redondeadas con `border_radius`.
- Texto con `pygame.font`: `render()` crea la imagen del texto y `blit()` la pega en pantalla.

---

### [`03_movimiento_teclado.py`](03_movimiento_teclado.py)
**Qué hace:** un cuadro que se mueve con las flechas o con WASD y no puede salirse de la ventana.

**Conceptos que enseña:**
- `pygame.Rect`: posición y tamaño de un objeto.
- `pygame.key.get_pressed()`: saber qué teclas están sostenidas.
- **Delta time (`dt`)**: mover por segundo y no por cuadro, para que la velocidad sea igual en cualquier computadora.
- `clamp_ip()`: mantener un objeto dentro de los límites de la pantalla.

---

### [`04_mouse_y_eventos.py`](04_mouse_y_eventos.py)
**Qué hace:** lienzo interactivo. Clic izquierdo crea círculos de colores, clic derecho los borra, la rueda cambia el tamaño y la barra espaciadora cambia el fondo.

**Conceptos que enseña:**
- Eventos `MOUSEBUTTONDOWN`, `MOUSEWHEEL` y `KEYDOWN`.
- Diferenciar botones del mouse (`evento.button`).
- `pygame.mouse.get_pos()`: posición actual del cursor.
- Guardar objetos en listas y dibujarlos cada cuadro.

---

### [`05_colisiones.py`](05_colisiones.py)
**Qué hace:** mueves un cuadro azul entre obstáculos que funcionan como paredes y recoges monedas que suman puntos.

**Conceptos que enseña:**
- `Rect.colliderect()`: detectar si dos rectángulos se tocan.
- `Rect.collidelist()`: revisar colisiones contra una lista completa.
- Guardar la posición anterior con `copy()` para deshacer un movimiento que choca.
- Marcador de puntos y mensaje al ganar.

---

### [`06_sprites_y_grupos.py`](06_sprites_y_grupos.py)
**Qué hace:** caen gotas del cielo y tú controlas un recipiente con las flechas para atraparlas.

**Conceptos que enseña:**
- Programación orientada a objetos con `pygame.sprite.Sprite`.
- Los atributos `image` y `rect` de un sprite.
- `pygame.sprite.Group`: actualizar y dibujar muchos objetos con una sola instrucción.
- `spritecollide()`: colisiones entre un sprite y un grupo.
- `kill()`: eliminar un sprite.
- Eventos propios con `USEREVENT` y `pygame.time.set_timer()`.
- Dibujar sprites con código, sin archivos de imagen.

---

### [`07_sonido_generado.py`](07_sonido_generado.py)
**Qué hace:** un pequeño piano. Las teclas `1` a `8` tocan las notas Do–Do y la barra espaciadora produce un efecto de láser.

**Conceptos que enseña:**
- `pygame.mixer` y `pygame.mixer.Sound`.
- Generar sonidos con matemáticas (onda senoidal) en vez de usar archivos de audio.
- Manejo de errores con `try/except` si el equipo no tiene salida de audio.
- Reaccionar a una sola pulsación con `KEYDOWN`.

---

### [`08_juego_esquiva_meteoros.py`](08_juego_esquiva_meteoros.py) 🚀 (el videojuego)
**Qué hace:** juego espacial completo. Pilotas una nave, esquivas o destruyes meteoros y atrapas estrellas para sumar puntos. Cada 15 segundos sube el nivel y todo se vuelve más difícil.

**Controles**

| Tecla | Acción |
|---|---|
| Flechas / WASD | Mover la nave |
| `ESPACIO` | Disparar (mantenlo presionado) |
| `ENTER` | Empezar / jugar de nuevo |
| `P` | Pausa |
| `ESC` | Salir |

**Reglas**
- Empiezas con **3 vidas**; cada choque con un meteoro te quita una y la nave parpadea un momento sin poder ser dañada.
- Destruir un meteoro con un disparo da **+5 puntos**.
- Atrapar una estrella da **+20 puntos**; cada 3 estrellas recuperas una vida si te falta alguna.
- Sobrevivir también suma puntos con el tiempo.
- Al perder, el juego muestra tu puntaje y guarda el **récord** de la sesión.

**Cómo está hecho**
- **Máquina de estados** (`MENU`, `JUGANDO`, `PAUSA`, `FIN`) para controlar qué pantalla se muestra.
- Clase `Juego` que organiza reinicio, actualización, dibujo y bucle principal.
- Cuatro clases de sprites: `Jugador`, `Meteoro`, `Estrella` y `Bala`.
- Grupos de sprites y `groupcollide()` / `spritecollide()` para las colisiones; `collide_circle` para golpes más justos.
- Dificultad progresiva: el intervalo de aparición y la velocidad de los meteoros dependen del nivel.
- Fondo de estrellas con tres velocidades para dar sensación de profundidad.
- Movimiento con `Vector2` y delta time, con movimiento diagonal normalizado.
- Interfaz (HUD) con puntos, nivel, vidas y récord, además de pantallas de inicio, pausa y Game Over.
- Todos los gráficos se dibujan con código.

---

## 🧠 Glosario rápido

| Término | Significado |
|---|---|
| **Game loop** | Ciclo que se repite sin parar: leer eventos, actualizar el juego y dibujar. |
| **FPS** | Cuadros por segundo. |
| **Surface** | Superficie donde se dibuja (la pantalla es una). |
| **Rect** | Rectángulo con posición y tamaño; base de las colisiones. |
| **Sprite** | Objeto del juego con imagen y posición (jugador, enemigo, bala...). |
| **Group** | Colección de sprites que se actualiza y dibuja junta. |
| **Delta time (dt)** | Tiempo entre un cuadro y otro; permite velocidad constante en cualquier equipo. |
| **Blit** | "Pegar" una imagen o superficie sobre otra. |

## 📖 Recursos para seguir aprendiendo

- [Documentación oficial de Pygame](https://www.pygame.org/docs/)
- [Sitio oficial de Pygame](https://www.pygame.org/)

## 📄 Licencia

Distribuido bajo licencia MIT. Consulta el archivo `LICENSE`.
