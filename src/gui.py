from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk, messagebox

from juego import (
    Arma,
    Comida,
    Enemigo,
    Jugador,
    Personaje,
    generar_enemigo,
    guardar_resultado,
)


# =====================================================
# COLORES Y ESTILOS
# =====================================================

COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#2a2a3d"
COLOR_TEXTO = "#f5f5f5"
COLOR_ACENTO = "#7aa2f7"
COLOR_OK = "#9ece6a"
COLOR_ERROR = "#f7768e"

COLOR_OCULTO = "#11111b"
COLOR_VISITADA = "#3b3b54"
COLOR_BORDE = "#1e1e2e"
COLOR_JUGADOR = "#7aa2f7"
COLOR_COMIDA = "#9ece6a"
COLOR_ARMA = "#e0af68"
COLOR_ENEMIGO = "#f7768e"
COLOR_SALIDA = "#bb9af7"
COLOR_RASTRO = "#6c7086"

FUENTE_TITULO = ("Helvetica", 18, "bold")
FUENTE_NORMAL = ("Helvetica", 11)
FUENTE_LOG = ("Courier", 10)
FUENTE_CELDA = ("Helvetica", 14)

GRID_SIZE = 10
CELDA_PX = 32

# tipos: "nada", "comida", "arma", "enemigo", "salida"
ICONO_CELDA = {
    "nada": ("", COLOR_VISITADA),
    "comida": ("🍖", COLOR_COMIDA),
    "arma": ("⚔", COLOR_ARMA),
    "enemigo": ("👾", COLOR_ENEMIGO),
    "salida": ("🚪", COLOR_SALIDA),
}


# =====================================================
# MAPA
# =====================================================

class Mapa:

    def __init__(self, tamanio: int = GRID_SIZE) -> None:

        self.tamanio: int = tamanio
        self.celdas: dict[tuple[int, int], str] = {}
        self.visitadas: set[tuple[int, int]] = set()
        self.rastros: dict[tuple[int, int], str] = {}

        for x in range(tamanio):
            for y in range(tamanio):
                self.celdas[(x, y)] = self._generar_tipo()

        # el inicio siempre seguro y visitado
        self.celdas[(0, 0)] = "nada"
        self.visitadas.add((0, 0))

        # asegurar al menos una salida
        while True:
            x = random.randint(0, tamanio - 1)
            y = random.randint(0, tamanio - 1)

            if (x, y) != (0, 0):
                self.celdas[(x, y)] = "salida"
                break

    def _generar_tipo(self) -> str:

        n = random.randint(1, 100)

        if n <= 55:
            return "nada"
        elif n <= 70:
            return "comida"
        elif n <= 85:
            return "arma"
        elif n <= 97:
            return "enemigo"
        else:
            return "salida"

    def en_rango(self, x: int, y: int) -> bool:
        return 0 <= x < self.tamanio and 0 <= y < self.tamanio

    def visitar(self, x: int, y: int) -> str:
        self.visitadas.add((x, y))
        return self.celdas[(x, y)]

    def consumir(self, x: int, y: int) -> None:
        self.rastros[(x, y)] = self.celdas[(x, y)]
        self.celdas[(x, y)] = "nada"


# =====================================================
# HELPER DE BOTON (compatible con macOS)
# =====================================================

def crear_boton(parent, texto, comando, color=COLOR_PANEL, width=12):

    return tk.Button(
        parent,
        text=texto,
        font=FUENTE_NORMAL,
        highlightbackground=color,
        width=width,
        command=comando,
    )


# =====================================================
# VALIDACIONES
# =====================================================

def validar_nombre(nombre: str) -> tuple[bool, str]:

    nombre = nombre.strip()

    if len(nombre) == 0:
        return False, "El nombre no puede estar vacio"

    if len(nombre) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"

    if len(nombre) > 20:
        return False, "El nombre no puede tener mas de 20 caracteres"

    for letra in nombre:
        if not (letra.isalpha() or letra.isspace()):
            return False, "El nombre solo puede tener letras"

    return True, nombre


def validar_genero(genero: str) -> tuple[bool, str]:

    genero = genero.strip().upper()

    if genero not in ("M", "F"):
        return False, "El genero debe ser M o F"

    return True, genero


# =====================================================
# VENTANA PRINCIPAL
# =====================================================

class JuegoGUI:

    def __init__(self, root: tk.Tk) -> None:

        self.root = root
        self.root.title("Juego POO")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("1080x640")
        self.root.resizable(False, False)

        self.jugador: Jugador | None = None
        self.mapa: Mapa | None = None
        self.juego_terminado: bool = False

        self.pantalla_inicio()

    # -------------------------------------------------
    # UTILIDADES UI
    # -------------------------------------------------

    def limpiar(self) -> None:

        for widget in self.root.winfo_children():
            widget.destroy()

    def log(self, texto: str, color: str = COLOR_TEXTO) -> None:

        self.texto_log.config(state="normal")
        self.texto_log.insert("end", texto + "\n", color)
        self.texto_log.tag_config(color, foreground=color)
        self.texto_log.see("end")
        self.texto_log.config(state="disabled")

    # -------------------------------------------------
    # PANTALLA DE INICIO
    # -------------------------------------------------

    def pantalla_inicio(self) -> None:

        self.limpiar()

        contenedor = tk.Frame(self.root, bg=COLOR_FONDO)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            contenedor,
            text="JUEGO POO",
            font=FUENTE_TITULO,
            fg=COLOR_ACENTO,
            bg=COLOR_FONDO,
        ).pack(pady=(0, 20))

        tk.Label(
            contenedor,
            text="Nombre:",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w")

        entry_nombre = tk.Entry(contenedor, font=FUENTE_NORMAL, width=30)
        entry_nombre.pack(pady=(0, 15))
        entry_nombre.focus()

        tk.Label(
            contenedor,
            text="Genero:",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w")

        genero_var = tk.StringVar(value="")

        frame_genero = tk.Frame(contenedor, bg=COLOR_FONDO)
        frame_genero.pack(pady=(0, 20))

        tk.Radiobutton(
            frame_genero,
            text="Masculino",
            variable=genero_var,
            value="M",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            selectcolor=COLOR_PANEL,
            activebackground=COLOR_FONDO,
            activeforeground=COLOR_ACENTO,
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_genero,
            text="Femenino",
            variable=genero_var,
            value="F",
            font=FUENTE_NORMAL,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            selectcolor=COLOR_PANEL,
            activebackground=COLOR_FONDO,
            activeforeground=COLOR_ACENTO,
        ).pack(side="left", padx=10)

        def iniciar() -> None:

            ok_nombre, valor_nombre = validar_nombre(entry_nombre.get())

            if not ok_nombre:
                messagebox.showerror("Nombre invalido", valor_nombre)
                return

            ok_genero, valor_genero = validar_genero(genero_var.get())

            if not ok_genero:
                messagebox.showerror("Genero invalido", valor_genero)
                return

            self.jugador = Jugador(valor_nombre, valor_genero)
            self.mapa = Mapa()
            self.pantalla_juego()

        crear_boton(contenedor, "Iniciar", iniciar, color=COLOR_ACENTO, width=20).pack()
        crear_boton(contenedor, "Ver Top 5", self.ventana_top5, width=20).pack(pady=10)

    # -------------------------------------------------
    # PANTALLA DE JUEGO
    # -------------------------------------------------

    def pantalla_juego(self) -> None:

        self.limpiar()
        self.juego_terminado = False

        # PANEL DE STATS

        panel_stats = tk.Frame(self.root, bg=COLOR_PANEL, padx=15, pady=10)
        panel_stats.pack(fill="x", padx=10, pady=10)

        self.lbl_nombre = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_ACENTO, bg=COLOR_PANEL
        )
        self.lbl_nombre.grid(row=0, column=0, sticky="w", padx=10)

        self.lbl_vida = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_OK, bg=COLOR_PANEL
        )
        self.lbl_vida.grid(row=0, column=1, sticky="w", padx=10)

        self.lbl_puntos = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_PANEL
        )
        self.lbl_puntos.grid(row=0, column=2, sticky="w", padx=10)

        self.lbl_pos = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_PANEL
        )
        self.lbl_pos.grid(row=1, column=0, sticky="w", padx=10)

        self.lbl_turnos = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_PANEL
        )
        self.lbl_turnos.grid(row=1, column=1, sticky="w", padx=10)

        self.lbl_distancia = tk.Label(
            panel_stats, font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_PANEL
        )
        self.lbl_distancia.grid(row=1, column=2, sticky="w", padx=10)

        # CONTENIDO PRINCIPAL: MAPA + LOG

        cuerpo = tk.Frame(self.root, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True, padx=10)

        # MAPA (CANVAS)

        lado = GRID_SIZE * CELDA_PX

        self.canvas = tk.Canvas(
            cuerpo,
            width=lado,
            height=lado,
            bg=COLOR_FONDO,
            highlightthickness=0,
        )
        self.canvas.pack(side="left", padx=(0, 10))
        self.canvas.bind("<Button-1>", self.on_click_mapa)

        # LOG

        frame_log = tk.Frame(cuerpo, bg=COLOR_FONDO)
        frame_log.pack(side="right", fill="both", expand=True)

        self.texto_log = tk.Text(
            frame_log,
            font=FUENTE_LOG,
            bg="#11111b",
            fg=COLOR_TEXTO,
            height=15,
            state="disabled",
            wrap="word",
        )
        self.texto_log.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(frame_log, command=self.texto_log.yview)
        scroll.pack(side="right", fill="y")
        self.texto_log.config(yscrollcommand=scroll.set)

        # BOTONES

        panel_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        panel_botones.pack(pady=10)

        botones = [
            ("Arriba", lambda: self.accion_mover("w")),
            ("Abajo", lambda: self.accion_mover("s")),
            ("Izquierda", lambda: self.accion_mover("a")),
            ("Derecha", lambda: self.accion_mover("d")),
            ("Inventario", self.accion_inventario),
            ("Usar comida", self.accion_usar_comida),
            ("Botar item", self.accion_botar_item),
            ("Salir", self.accion_salir),
        ]

        for i, (texto, comando) in enumerate(botones):

            crear_boton(panel_botones, texto, comando).grid(
                row=i // 4, column=i % 4, padx=4, pady=4
            )

        self.actualizar_stats()
        self.dibujar_mapa()

        self.log("===== JUEGO INICIADO =====", COLOR_ACENTO)
        self.log(f"Bienvenido {self.jugador.nombre}")
        self.log(f"Vida: {self.jugador.vida} | Danio base: {self.jugador.damage}")
        self.log("Muevete con los botones o tocando una celda vecina")

    # -------------------------------------------------
    # ACTUALIZAR STATS
    # -------------------------------------------------

    def actualizar_stats(self) -> None:

        j = self.jugador

        self.lbl_nombre.config(text=f"Jugador: {j.nombre} ({j.genero})")
        self.lbl_vida.config(text=f"Vida: {j.vida}")
        self.lbl_puntos.config(text=f"Puntos: {j.puntos}")
        self.lbl_pos.config(text=f"Posicion: ({j.posicion_x}, {j.posicion_y})")
        self.lbl_turnos.config(text=f"Turnos: {j.turnos}/60")
        self.lbl_distancia.config(text=f"Distancia: {j.distancia_total}")

    # -------------------------------------------------
    # ACCIONES
    # -------------------------------------------------

    def accion_mover(self, direccion: str) -> None:

        if self.juego_terminado:
            return

        j = self.jugador

        nuevo_x = j.posicion_x
        nuevo_y = j.posicion_y

        if direccion == "d":
            nuevo_x += 1
        elif direccion == "a":
            nuevo_x -= 1
        elif direccion == "w":
            nuevo_y += 1
        elif direccion == "s":
            nuevo_y -= 1

        if not self.mapa.en_rango(nuevo_x, nuevo_y):
            self.log("No puedes salir del mapa", COLOR_ERROR)
            return

        j.posicion_x = nuevo_x
        j.posicion_y = nuevo_y

        j.distancia_total += 1
        j.turnos += 1

        self.log(f"\nTe moviste a ({j.posicion_x}, {j.posicion_y})", COLOR_ACENTO)

        tipo = self.mapa.visitar(j.posicion_x, j.posicion_y)

        self.actualizar_stats()
        self.dibujar_mapa()

        self.disparar_evento(tipo)

        if j.vida <= 0:
            self.terminar_juego("perdio")
            return

        if self.juego_terminado:
            return

        if j.turnos >= 60:
            self.log("\nSOBREVIVISTE 60 TURNOS", COLOR_OK)
            self.terminar_juego("gano")

    def on_click_mapa(self, event) -> None:

        if self.juego_terminado:
            return

        cx = event.x // CELDA_PX
        cy_canvas = event.y // CELDA_PX

        # invertir Y porque el canvas crece hacia abajo
        cy = (GRID_SIZE - 1) - cy_canvas

        if not self.mapa.en_rango(cx, cy):
            return

        dx = cx - self.jugador.posicion_x
        dy = cy - self.jugador.posicion_y

        if abs(dx) + abs(dy) != 1:
            self.log("Solo puedes moverte a una celda vecina", COLOR_ERROR)
            return

        if dx == 1:
            self.accion_mover("d")
        elif dx == -1:
            self.accion_mover("a")
        elif dy == 1:
            self.accion_mover("w")
        elif dy == -1:
            self.accion_mover("s")

    def accion_inventario(self) -> None:

        if len(self.jugador.inventario) == 0:
            self.log("Inventario vacio")
            return

        self.log("\n----- INVENTARIO -----")

        for i, item in enumerate(self.jugador.inventario):
            self.log(f"{i}. {item}")

    def accion_usar_comida(self) -> None:

        if self.juego_terminado:
            return

        comidas = [
            item for item in self.jugador.inventario if isinstance(item, Comida)
        ]

        if len(comidas) == 0:
            messagebox.showinfo("Sin comida", "No tienes comida en el inventario")
            return

        opciones = [str(c) for c in comidas]
        indice = self.seleccionar_opcion("Selecciona comida", opciones)

        if indice is None:
            return

        comida = comidas[indice]

        vida_antes = self.jugador.vida
        self.jugador.vida += comida.cura
        recuperado = self.jugador.vida - vida_antes

        self.log(f"Usaste {comida.nombre} (+{recuperado} vida)", COLOR_OK)

        indice_real = list(self.jugador.inventario).index(comida)
        self.jugador.inventario.eliminar_item(indice_real)

        self.actualizar_stats()

    def accion_botar_item(self) -> None:

        if self.juego_terminado:
            return

        if len(self.jugador.inventario) == 0:
            messagebox.showinfo("Inventario vacio", "No tienes items para botar")
            return

        opciones = [str(item) for item in self.jugador.inventario]
        indice = self.seleccionar_opcion("Selecciona item a botar", opciones)

        if indice is None:
            return

        item = self.jugador.inventario.obtener_item(indice)
        self.jugador.inventario.eliminar_item(indice)

        self.log(f"Botaste {item}", COLOR_ERROR)

    def accion_salir(self) -> None:

        if messagebox.askyesno("Salir", "Seguro que quieres salir del juego?"):
            self.root.destroy()

    # -------------------------------------------------
    # EVENTO POR CELDA
    # -------------------------------------------------

    def disparar_evento(self, tipo: str) -> None:

        x, y = self.jugador.posicion_x, self.jugador.posicion_y

        if tipo == "nada":
            self.log("No ocurrio nada")

        elif tipo == "comida":

            comidas = [
                Comida("Pan", random.randint(1, 5)),
                Comida("Carne", random.randint(1, 5)),
                Comida("Fruta", random.randint(1, 5)),
            ]

            comida = random.choice(comidas)

            self.log(f"Encontraste comida: {comida}")

            if messagebox.askyesno("Comida", f"Encontraste {comida}\nQuieres recogerla?"):

                agregado = self.jugador.inventario.agregar_item(comida)

                if not agregado:
                    self.log("Inventario lleno", COLOR_ERROR)
                else:
                    self.log(f"Recogiste {comida}", COLOR_OK)

            self.mapa.consumir(x, y)
            self.dibujar_mapa()

        elif tipo == "arma":

            armas = [
                Arma("Cuchillo", 10, 20),
                Arma("Ballesta", 20, 15),
                Arma("Escopeta", 30, 10),
            ]

            arma = random.choice(armas)

            self.log(f"Encontraste un arma: {arma}")

            if messagebox.askyesno("Arma", f"Encontraste {arma}\nQuieres recogerla?"):

                agregado = self.jugador.inventario.agregar_item(arma)

                if not agregado:
                    self.log("Inventario lleno", COLOR_ERROR)
                else:
                    self.log(f"Recogiste {arma}", COLOR_OK)

            self.mapa.consumir(x, y)
            self.dibujar_mapa()

        elif tipo == "enemigo":

            enemigo = generar_enemigo()
            self.log(f"\nAparecio un enemigo: {enemigo.nombre}", COLOR_ERROR)
            self.combate(enemigo)

            self.mapa.consumir(x, y)
            self.dibujar_mapa()

        elif tipo == "salida":

            self.log("\nENCONTRASTE LA SALIDA", COLOR_OK)
            self.terminar_juego("gano")

    # -------------------------------------------------
    # DIBUJAR MAPA
    # -------------------------------------------------

    def dibujar_mapa(self) -> None:

        self.canvas.delete("all")

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):

                # invertir Y para que +y se dibuje hacia arriba
                cy = (GRID_SIZE - 1) - y

                x1 = x * CELDA_PX
                y1 = cy * CELDA_PX
                x2 = x1 + CELDA_PX
                y2 = y1 + CELDA_PX

                if (x, y) in self.mapa.visitadas:

                    tipo = self.mapa.celdas[(x, y)]
                    letra, color = ICONO_CELDA[tipo]

                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=COLOR_VISITADA, outline=COLOR_BORDE
                    )

                    if letra:
                        self.canvas.create_text(
                            x2 - 10,
                            y1 + 10,
                            text=letra,
                            fill=color,
                            font=FUENTE_CELDA,
                        )
                    elif (x, y) in self.mapa.rastros:
                        rastro_tipo = self.mapa.rastros[(x, y)]
                        rastro_letra, _ = ICONO_CELDA[rastro_tipo]
                        self.canvas.create_text(
                            x2 - 10,
                            y1 + 10,
                            text=rastro_letra,
                            fill=COLOR_RASTRO,
                            font=FUENTE_CELDA,
                        )

                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=COLOR_OCULTO, outline=COLOR_BORDE
                    )

        # dibujar al jugador como un maguito
        jx = self.jugador.posicion_x
        jy = (GRID_SIZE - 1) - self.jugador.posicion_y

        x1 = jx * CELDA_PX
        y1 = jy * CELDA_PX

        # tunica
        self.canvas.create_polygon(
            x1 + CELDA_PX * 0.5, y1 + CELDA_PX * 0.55,
            x1 + CELDA_PX * 0.12, y1 + CELDA_PX * 0.95,
            x1 + CELDA_PX * 0.88, y1 + CELDA_PX * 0.95,
            fill=COLOR_ACENTO,
            outline=COLOR_TEXTO,
        )

        # cabeza
        self.canvas.create_oval(
            x1 + CELDA_PX * 0.32, y1 + CELDA_PX * 0.30,
            x1 + CELDA_PX * 0.68, y1 + CELDA_PX * 0.58,
            fill="#f5deb3",
            outline=COLOR_TEXTO,
        )

        # sombrero
        self.canvas.create_polygon(
            x1 + CELDA_PX * 0.5, y1 + CELDA_PX * 0.02,
            x1 + CELDA_PX * 0.22, y1 + CELDA_PX * 0.36,
            x1 + CELDA_PX * 0.78, y1 + CELDA_PX * 0.36,
            fill="#bb9af7",
            outline=COLOR_TEXTO,
        )

    # -------------------------------------------------
    # COMBATE
    # -------------------------------------------------

    def combate(self, enemigo: Enemigo) -> None:

        self.log("===== COMBATE =====", COLOR_ACENTO)

        armas = [
            item for item in self.jugador.inventario if isinstance(item, Arma)
        ]

        if len(armas) == 0:

            self.log("No tienes armas, atacas con las manos")
            dano_jugador = self.jugador.damage // 2

        else:

            opciones = [str(a) for a in armas]
            indice = self.seleccionar_opcion("Selecciona arma", opciones)

            if indice is None:
                self.log("No atacaste, peleas con las manos")
                dano_jugador = self.jugador.damage // 2
            else:
                arma = armas[indice]
                dano_arma = arma.atacar()

                if dano_arma == 0:
                    self.log(f"La {arma.nombre} fallo", COLOR_ERROR)

                dano_jugador = Personaje.calcular_danio(self.jugador.damage, dano_arma)

        if enemigo.esquivar():
            self.log(f"{enemigo.nombre} esquivo el ataque", COLOR_ERROR)
            dano_jugador = 0

        dano_enemigo = enemigo.atacar()

        self.log(f"Danio jugador: {dano_jugador}")
        self.log(f"Danio enemigo: {dano_enemigo}")

        if dano_jugador > dano_enemigo:

            puntos_ganados = random.randint(50, 150)
            self.jugador.puntos += puntos_ganados

            self.log(f"Ganaste contra {enemigo.nombre} (+{puntos_ganados} pts)", COLOR_OK)

        else:

            self.log("Perdiste el combate", COLOR_ERROR)
            self.jugador.vida = 0

        self.actualizar_stats()

    # -------------------------------------------------
    # SELECCIONAR OPCION (MODAL)
    # -------------------------------------------------

    def seleccionar_opcion(self, titulo: str, opciones: list[str]) -> int | None:

        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("320x260")
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(
            ventana,
            text=titulo,
            font=FUENTE_NORMAL,
            fg=COLOR_ACENTO,
            bg=COLOR_FONDO,
        ).pack(pady=10)

        lista = tk.Listbox(
            ventana,
            font=FUENTE_NORMAL,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            selectbackground=COLOR_ACENTO,
            height=8,
        )
        lista.pack(fill="both", expand=True, padx=15, pady=5)

        for opcion in opciones:
            lista.insert("end", opcion)

        lista.selection_set(0)

        seleccion = {"indice": None}

        def aceptar() -> None:

            sel = lista.curselection()

            if len(sel) == 0:
                messagebox.showwarning("Sin seleccion", "Debes seleccionar una opcion", parent=ventana)
                return

            seleccion["indice"] = sel[0]
            ventana.destroy()

        def cancelar() -> None:
            ventana.destroy()

        frame_btns = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_btns.pack(pady=10)

        crear_boton(frame_btns, "Aceptar", aceptar, color=COLOR_ACENTO, width=10).pack(
            side="left", padx=5
        )
        crear_boton(frame_btns, "Cancelar", cancelar, width=10).pack(side="left", padx=5)

        self.root.wait_window(ventana)

        return seleccion["indice"]

    # -------------------------------------------------
    # FIN DEL JUEGO
    # -------------------------------------------------

    def terminar_juego(self, resultado: str) -> None:

        if self.juego_terminado:
            return

        self.juego_terminado = True

        if resultado == "gano":
            self.jugador.puntos += 250
            self.log("\n===== GANASTE =====", COLOR_OK)
            self.log("Bono por ganar: +250 pts", COLOR_OK)
        else:
            self.log("\n===== GAME OVER =====", COLOR_ERROR)

        self.actualizar_stats()

        self.log(f"Puntos finales: {self.jugador.puntos}")
        self.log(f"Distancia recorrida: {self.jugador.distancia_total}")

        guardar_resultado(self.jugador, resultado)

        self.ventana_top5(mostrar_volver=True)

    def reiniciar(self) -> None:

        self.jugador = None
        self.mapa = None
        self.juego_terminado = False
        self.pantalla_inicio()

    # -------------------------------------------------
    # VENTANA TOP 5
    # -------------------------------------------------

    def ventana_top5(self, mostrar_volver: bool = False) -> None:

        ventana = tk.Toplevel(self.root)
        ventana.title("Top 5")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("400x340")
        ventana.transient(self.root)

        tk.Label(
            ventana,
            text="TOP 5",
            font=FUENTE_TITULO,
            fg=COLOR_ACENTO,
            bg=COLOR_FONDO,
        ).pack(pady=10)

        texto = tk.Text(
            ventana,
            font=FUENTE_LOG,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            height=10,
            state="normal",
            wrap="word",
        )
        texto.pack(fill="both", expand=True, padx=15, pady=5)

        import json

        try:
            with open("puntajes.json", "r") as archivo:
                puntajes = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            puntajes = []

        if len(puntajes) == 0:
            texto.insert("end", "No hay puntajes guardados\n")
        else:
            puntajes.sort(key=lambda x: x["puntos"], reverse=True)

            for i, jug in enumerate(puntajes[:5], start=1):
                texto.insert(
                    "end",
                    f"{i}. {jug['nombre']} | "
                    f"Puntos: {jug['puntos']} | "
                    f"Resultado: {jug['resultado']}\n",
                )

        texto.config(state="disabled")

        frame_btns = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_btns.pack(pady=10)

        if mostrar_volver:

            def volver() -> None:
                ventana.destroy()
                self.reiniciar()

            crear_boton(
                frame_btns, "Volver a jugar", volver, color=COLOR_ACENTO, width=14
            ).pack(side="left", padx=5)

        crear_boton(
            frame_btns, "Cerrar", ventana.destroy, width=10
        ).pack(side="left", padx=5)


# =====================================================
# MAIN
# =====================================================

def main() -> None:

    root = tk.Tk()
    JuegoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
