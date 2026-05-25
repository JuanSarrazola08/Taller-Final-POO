from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


# =====================================================
# COLORES Y ESTILOS
# =====================================================

COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#2a2a3d"
COLOR_TEXTO = "#f5f5f5"
COLOR_ACENTO = "#7aa2f7"
COLOR_OK = "#9ece6a"
COLOR_ERROR = "#f7768e"

FUENTE_TITULO = ("Helvetica", 18, "bold")
FUENTE_NORMAL = ("Helvetica", 11)
FUENTE_LOG = ("Courier", 10)


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
        self.root.geometry("720x560")
        self.root.resizable(False, False)

        self.pantalla_inicio()

    def limpiar(self) -> None:

        for widget in self.root.winfo_children():
            widget.destroy()

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

            messagebox.showinfo("Listo", f"Bienvenido {valor_nombre} ({valor_genero})")

        crear_boton(contenedor, "Iniciar", iniciar, color=COLOR_ACENTO, width=20).pack()
        crear_boton(contenedor, "Ver Top 5", self.ventana_top5, width=20).pack(pady=10)

    # -------------------------------------------------
    # VENTANA TOP 5
    # -------------------------------------------------

    def ventana_top5(self) -> None:

        ventana = tk.Toplevel(self.root)
        ventana.title("Top 5")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("400x300")
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

        crear_boton(
            ventana, "Cerrar", ventana.destroy, color=COLOR_ACENTO, width=10
        ).pack(pady=10)


# =====================================================
# MAIN
# =====================================================

def main() -> None:

    root = tk.Tk()
    JuegoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
