# Taller-Final-POO

Mi proyecto final consiste en un juego llamado "Mundo Oscuro" donde el jugador se mueve por un mapa y, al desplazarse, pueden ocurrir eventos aleatorios (enemigos, comida, armas) y existe una baja probabilidad de encontrar la salida.

Contenido
- Código original del juego (consola) añadido en [src/juego.py](src/juego.py#L1-L400).

Estructura propuesta del proyecto
- src/: código fuente
	- juego.py        -> Código que proporcionaste (modelo y lógica de la consola)
- puntajes.json     -> creado en tiempo de ejecución (almacena resultados)
- requirements.txt  -> dependencias recomendadas

Arquitectura sugerida
Propongo seguir una separación por capas (Modelo — Juego/Engine — Interfaz), inspirada en MVC:

- Modelo (`models/`): clases puras del dominio (`Personaje`, `Jugador`, `Enemigo`, `Arma`, `Comida`, `Inventario`). Actualmente están dentro de `src/juego.py`.
- Lógica del juego / motor (`engine/`): funciones que controlan el flujo del juego (`generar_enemigo`, `combate`, `evento_random`, `guardar_resultado`, `mostrar_top5`). Estas funciones deben poder ejecutarse sin dependencia de la consola (sin `input()` ni `print()` para la lógica central).
- Interfaz (`ui/`): aquí irá la capa gráfica (pantallas, renderizado, manejo de eventos). Reemplazará llamadas a `input()` y `print()` por eventos, callbacks y renderizado en pantalla.

Beneficios:
- Facilita probar la lógica sin UI.
- Permite múltiples frontends (consola, pygame, tkinter) reutilizando la misma lógica.

Pasos recomendados para pasar a interfaz gráfica (ejemplo con `pygame` — recomendado para juegos más visuales):

1. Refactorizar el código actual en módulos:
	 - `src/models.py` — todas las clases (sin llamadas a `input()`/`print()` dentro de la lógica de modelo).
	 - `src/engine.py` — funciones `generar_enemigo`, `combate`, `evento_random`, `guardar_resultado`, `mostrar_top5` (recibiendo callbacks o retornando eventos en vez de interactuar con la consola).
	 - `src/main.py` — punto de arranque que inicializa la interfaz y el bucle del juego.
2. Diseñar un `Game` o `Controller` que mantenga el estado (jugador actual, pantalla activa, puntajes) y exponga métodos como `update(dt)`, `handle_event(ev)`, `render(screen)`.
3. Implementar pantallas (estados) para: `Menu`, `Juego`, `GameOver`, `Top5`.
4. Reemplazar menús de texto por botones/teclas y HUD para mostrar vida, puntos y distancia en tiempo real.
5. Integrar guardado de puntajes usando la misma `guardar_resultado`, llamada desde el `Game` al terminar la partida.

Alternativa ligera: `tkinter` si quieres interfaces con controles nativos (botones, labels) y menos trabajo con render loop. `pygame` ofrece mayor control y animaciones.

Dependencias sugeridas
- pygame>=2.1.3  # si eliges pygame

Cómo ejecutar (actual, en consola)

1. Crear y activar un entorno virtual:

`python -m venv venv`

`venv\\Scripts\\activate` (Windows PowerShell: `venv\\Scripts\\Activate.ps1`)

2. Ejecutar el juego de consola:

`python -m src.juego`

Siguientes tareas (priorizadas)
- Refactorizar clases a `src/models.py`.
- Mover lógica de juego a `src/engine.py` y eliminar dependencias de `input()`/`print()`.
- Elegir librería para UI (`pygame` recomendado) y crear `src/ui/main.py` con el bucle principal.
- Implementar pantalla de menú, pantalla de juego y pantalla de resultados.

Si quieres, puedo:
- Refactorizar automáticamente tu código en módulos (`models.py`, `engine.py`, `main.py`).
- Crear un esqueleto con `pygame` que muestre el HUD y permita mover al jugador y generar eventos.

