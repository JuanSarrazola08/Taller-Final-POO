# Taller-Final-POO

Juego de aventura en 2D llamado **"Mundo Oscuro"** donde el jugador se mueve por un mapa con cuadrícula, encuenra enemigos, comida, armas y busca la salida. Implementa una interfaz gráfica con pygame, gestión de inventario, combate por turnos y un sistema de puntajes persistente.

## Descripción del Proyecto

- **Género**: Juego de rol/aventura por turnos con exploración aleatoria
- **Mecánicas**: Movimiento en cuadrícula, combate, inventario, eventos aleatorios, sistema de puntuación
- **Tecnología**: Python 3.12+, Pygame 2.6+
- **Plataforma**: Windows, Linux, macOS

## Estructura del Proyecto

```
src/
├── models.py       # Clases del dominio (Personaje, Jugador, Enemigo, Arma, Comida, Inventario)
├── engine.py       # Lógica del juego (eventos, combate, guardado de puntajes)
├── ui/
│   └── main.py     # Interfaz gráfica con pygame (pantalla de inicio, juego, top 5)
└── juego.py        # Versión original del código (consola)

scripts/
└── auto_run_ui.py  # Script de prueba headless

requirements.txt    # Dependencias del proyecto
puntajes.json       # Almacenamiento de puntuaciones (creado en tiempo de ejecución)
```

## Dependencias

- **pygame** >= 2.1.3 — Motor gráfico para la interfaz 2D

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JuanSarrazola08/Taller-Final-POO.git
cd Taller-Final-POO
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución

### Ejecutar el juego con interfaz gráfica

```bash
python -m src.ui.main
```

### Ejecutar prueba automatizada (headless)

```bash
python scripts/auto_run_ui.py
```

## Cómo Jugar

- **Movimiento**: WASD o flechas del teclado
- **Ver inventario**: Tecla `I`
- **Usar comida**: Tecla `U`
- **Recoger items**: Tecla `Y` (sí) / `N` (no)
- **Salir**: Tecla `Q`
- **En pantalla de Game Over**: Tecla `ESC` (guarda y muestra Top 5)

## Objetivos del Juego

- Sobrevivir 40 turnos o encontrar la salida (probabilidad baja)
- Acumular puntos derrotando enemigos
- Administrar inventario (máx. 3 items)
- Gestionar salud comiendo alimentos

## Características Implementadas

- ✅ Interfaz gráfica con pygame
- ✅ Mapa con cuadrícula y sprite de mago
- ✅ Pantalla de inicio con validaciones
- ✅ Pantalla de juego con HUD (vida, puntos, distancia)
- ✅ Log de eventos y combates
- ✅ Gestión de inventario visual
- ✅ Guardado persistente de puntuaciones (JSON)
- ✅ Tabla de Top 5 puntuaciones

## Arquitectura

El proyecto sigue un patrón de capas:

- **Modelo** (`models.py`): Clases puras del dominio sin entrada/salida
- **Motor** (`engine.py`): Lógica de juego desacoplada de la UI
- **UI** (`ui/main.py`): Interfaz gráfica con manejo de eventos

Esto permite reutilizar la lógica con diferentes frontends (consola, web, etc.).

## Autor

**JuanSarrazola08**

## Licencia

Proyecto educativo — Taller Final Programación Orientada a Objetos

