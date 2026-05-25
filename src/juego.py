from __future__ import annotations

from abc import ABC, abstractmethod
import random
import json
from typing import Optional


# =====================================================
# CLASE ABSTRACTA PERSONAJE
# =====================================================

class Personaje(ABC):

    contador_personajes: int = 0

    def __init__(self, nombre: str, genero: str, vida: int, damage: int) -> None:

        self.nombre: str = nombre
        self.genero: str = genero
        self.damage: int = damage

        self.__vida: int = vida

        Personaje.contador_personajes += 1

    @property
    def vida(self) -> int:
        return self.__vida

    @vida.setter
    def vida(self, valor: int) -> None:

        if valor < 0:
            valor = 0

        self.__vida = valor

    @abstractmethod
    def atacar(self) -> int:
        pass

    @abstractmethod
    def mostrar_info(self) -> str:
        pass

    @staticmethod
    def calcular_danio(base: int, extra: int) -> int:
        return base + extra

    @classmethod
    def total_personajes(cls) -> int:
        return cls.contador_personajes

    def __str__(self) -> str:
        return f"{self.nombre} | Vida: {self.vida}"

    def __repr__(self) -> str:
        return f"Personaje(nombre={self.nombre}, vida={self.vida})"


# =====================================================
# COMIDA
# =====================================================

class Comida:

    def __init__(self, nombre: str, cura: int) -> None:

        self.nombre: str = nombre
        self.cura: int = cura

    def usar(self, jugador: Jugador) -> None:

        jugador.vida += self.cura

        print(f"{jugador.nombre} recupera {self.cura} de vida")

    def __str__(self) -> str:
        return f"{self.nombre} (+{self.cura} vida)"

    def __repr__(self) -> str:
        return f"Comida({self.nombre})"


# =====================================================
# ARMAS
# =====================================================

class Arma:

    def __init__(self, nombre: str, dano: int, probabilidad_fallo: int) -> None:

        self.nombre: str = nombre
        self.dano: int = dano
        self.probabilidad_fallo: int = probabilidad_fallo

    def atacar(self) -> int:

        fallo = random.randint(1, 100)

        if fallo <= self.probabilidad_fallo:
            print(f"La {self.nombre} fallo")
            return 0

        return self.dano

    def __str__(self) -> str:
        return f"{self.nombre} | Danio: {self.dano}"

    def __repr__(self) -> str:
        return f"Arma({self.nombre})"


# =====================================================
# INVENTARIO (COMPOSICION)
# =====================================================

class Inventario:

    def __init__(self, capacidad: int = 3) -> None:

        self.__items: list = []
        self.capacidad: int = capacidad

    def agregar_item(self, item) -> bool:

        if len(self.__items) >= self.capacidad:
            print("Inventario lleno")
            return False

        self.__items.append(item)
        print(f"Se agrego {item}")

        return True

    def eliminar_item(self, indice: int) -> None:

        self.__items.pop(indice)

    def obtener_item(self, indice: int):

        return self.__items[indice]

    def mostrar(self) -> None:

        if len(self.__items) == 0:
            print("Inventario vacio")
            return

        for i, item in enumerate(self.__items):
            print(f"{i}. {item}")

    def __len__(self) -> int:
        return len(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __str__(self) -> str:
        return f"Inventario con {len(self.__items)} items"


# =====================================================
# JUGADOR
# =====================================================

class Jugador(Personaje):

    def __init__(self, nombre: str, genero: str) -> None:

        vida_random = random.randint(80, 100)
        damage_random = random.randint(10, 30)

        super().__init__(nombre, genero, vida_random, damage_random)

        self.posicion_x: int = 0
        self.posicion_y: int = 0

        self.distancia_total: int = 0
        self.puntos: int = 0
        self.turnos: int = 0

        self.inventario: Inventario = Inventario()

    def mover(self, direccion: str) -> None:

        if direccion == "d":
            self.posicion_x += 1

        elif direccion == "a":
            self.posicion_x -= 1

        elif direccion == "w":
            self.posicion_y += 1

        elif direccion == "s":
            self.posicion_y -= 1

        self.distancia_total += 1
        self.turnos += 1

        print(f"\nCoordenadas: ({self.posicion_x}, {self.posicion_y})")
        print(f"Distancia recorrida: {self.distancia_total}")

    def atacar(self) -> int:

        armas = [item for item in self.inventario if isinstance(item, Arma)]

        if len(armas) == 0:
            print("No tienes armas")
            return self.damage // 2

        print("\nARMAS DISPONIBLES")

        for i, arma in enumerate(armas):
            print(f"{i}. {arma}")

        try:
            opcion = int(input("Selecciona arma: "))
            arma = armas[opcion]

            dano = arma.atacar()

            dano_total = Personaje.calcular_danio(self.damage, dano)

            return dano_total

        except:
            print("Opcion invalida")
            return 0

    def usar_comida(self) -> None:

        comidas = [item for item in self.inventario if isinstance(item, Comida)]

        if len(comidas) == 0:
            print("No tienes comida")
            return

        print("\nCOMIDAS")

        for i, comida in enumerate(comidas):
            print(f"{i}. {comida}")

        try:
            opcion = int(input("Selecciona comida: "))

            comida = comidas[opcion]

            comida.usar(self)

            self.inventario.eliminar_item(
                self.inventario._Inventario__items.index(comida)
            )

        except:
            print("Opcion invalida")

    def botar_item(self) -> None:

        self.inventario.mostrar()

        if len(self.inventario) == 0:
            return

        try:
            opcion = int(input("Que item quieres botar: "))

            item = self.inventario.obtener_item(opcion)

            print(f"Botaste {item}")

            self.inventario.eliminar_item(opcion)

        except:
            print("Opcion invalida")

    def mostrar_info(self) -> str:

        return f"Jugador: {self.nombre} | Vida: {self.vida} | Puntos: {self.puntos}"


# =====================================================
# ENEMIGOS
# =====================================================

class Enemigo(Personaje):

    def __init__(self, nombre: str, vida: int, damage: int, resistencia: int) -> None:

        super().__init__(nombre, "M", vida, damage)

        self.resistencia: int = resistencia

    def esquivar(self) -> bool:

        probabilidad = random.randint(1, 100)

        return probabilidad <= 15

    def atacar(self) -> int:

        return self.damage

    def mostrar_info(self) -> str:

        return f"Enemigo: {self.nombre}"


class Sombra(Enemigo):

    def __init__(self) -> None:

        super().__init__("Sombra", 50, 10, 5)


class Bestia(Enemigo):

    def __init__(self) -> None:

        super().__init__("Bestia", 70, 15, 8)


class Titan(Enemigo):

    def __init__(self) -> None:

        super().__init__("Titan", 90, 20, 10)


class Demonio(Enemigo):

    def __init__(self) -> None:

        super().__init__("Demonio", 120, 25, 12)


# =====================================================
# FUNCION PARA CREAR ENEMIGOS RANDOM
# =====================================================


def generar_enemigo() -> Enemigo:

    enemigos = [
        Sombra(),
        Bestia(),
        Titan(),
        Demonio()
    ]

    return random.choice(enemigos)


# =====================================================
# GUARDAR PUNTAJES JSON
# =====================================================


def guardar_resultado(jugador: Jugador, resultado: str) -> None:

    datos = {
        "nombre": jugador.nombre,
        "puntos": jugador.puntos,
        "distancia": jugador.distancia_total,
        "resultado": resultado
    }

    try:

        with open("puntajes.json", "r") as archivo:
            puntajes = json.load(archivo)

    except (FileNotFoundError, json.JSONDecodeError):

        puntajes = []

    puntajes.append(datos)

    with open("puntajes.json", "w") as archivo:
        json.dump(puntajes, archivo, indent=4)

# =====================================================
# TOP 5
# =====================================================


def mostrar_top5() -> None:

    try:

        with open("puntajes.json", "r") as archivo:
            puntajes = json.load(archivo)

    except:
        print("No hay puntajes guardados")
        return

    puntajes.sort(key=lambda x: x["puntos"], reverse=True)

    print("\n===== TOP 5 =====")

    for i, jugador in enumerate(puntajes[:5], start=1):

        print(
            f"{i}. {jugador['nombre']} | "
            f"Puntos: {jugador['puntos']} | "
            f"Resultado: {jugador['resultado']}"
        )


# =====================================================
# EVENTOS RANDOM
# =====================================================


def evento_random(jugador: Jugador) -> Optional[str]:

    numero = random.randint(1, 100)

    # 40% nada
    if numero <= 40:
        print("No ocurrio nada")

    # 10% comida
    elif numero <= 50:

        comidas = [
            Comida("Pan", random.randint(1, 5)),
            Comida("Carne", random.randint(1, 5)),
            Comida("Fruta", random.randint(1, 5))
        ]

        comida = random.choice(comidas)

        print(f"Encontraste comida: {comida}")

        recoger = input("Deseas recogerla? (s/n): ")

        if recoger.lower() == "s":
            jugador.inventario.agregar_item(comida)

    # 10% arma
    elif numero <= 60:

        armas = [
            Arma("Cuchillo", 10, 20),
            Arma("Ballesta", 20, 15),
            Arma("Escopeta", 30, 10)
        ]

        arma = random.choice(armas)

        print(f"Encontraste un arma: {arma}")

        recoger = input("Deseas recogerla? (s/n): ")

        if recoger.lower() == "s":
            jugador.inventario.agregar_item(arma)

    # 40% enemigo
    else:

        enemigo = generar_enemigo()

        print(f"\nEncontraste un enemigo: {enemigo.nombre}")

        combate(jugador, enemigo)

        if jugador.vida <= 0:
            return "perdio"

    # salida aleatoria pequeña
    salida = random.randint(1, 100)

    if salida <= 5:
        print("\nENCONTRASTE LA SALIDA")
        return "gano"

    return None
    


# =====================================================
# COMBATE
# =====================================================


def combate(jugador: Jugador, enemigo: Enemigo) -> None:

    print("\n===== COMBATE =====")

    dano_jugador = jugador.atacar()

    if enemigo.esquivar():
        print(f"{enemigo.nombre} esquivo el ataque")
        dano_jugador = 0

    dano_enemigo = enemigo.atacar()

    print(f"Danio jugador: {dano_jugador}")
    print(f"Danio enemigo: {dano_enemigo}")

    if dano_jugador > dano_enemigo:

        print(f"Ganaste contra {enemigo.nombre}")

        puntos_ganados = random.randint(50, 150)

        jugador.puntos += puntos_ganados

        print(f"Ganaste {puntos_ganados} puntos")

    else:

        print("Perdiste el combate")

        jugador.vida = 0


# =====================================================
# MENU
# =====================================================


def mostrar_menu() -> None:

    print("\n===== MENU =====")
    print("1. Mover arriba")
    print("2. Mover abajo")
    print("3. Mover izquierda")
    print("4. Mover derecha")
    print("5. Ver inventario")
    print("6. Usar comida")
    print("7. Botar item")
    print("8. Ver puntos")
    print("9. Salir")


# =====================================================
# MAIN
# =====================================================


def main() -> None:

    print("===== JUEGO POO =====")

    nombre = input("Ingresa tu nombre: ")
    genero = input("Ingresa tu genero: ")

    jugador = Jugador(nombre, genero)

    print("\n===== PERSONAJE CREADO =====")
    print(f"Nombre: {jugador.nombre}")
    print(f"Genero: {jugador.genero}")
    print(f"Vida: {jugador.vida}")
    print(f"Danio base: {jugador.damage}")

    resultado = None

    while jugador.vida > 0:

        # gana por sobrevivir 40 turnos
        if jugador.turnos >= 40:
            print("\nSOBREVIVISTE 40 TURNOS")
            resultado = "gano"
            break

        mostrar_menu()

        opcion = input("Selecciona opcion: ")

        if opcion == "1":
            jugador.mover("w")
            resultado = evento_random(jugador)

        elif opcion == "2":
            jugador.mover("s")
            resultado = evento_random(jugador)

        elif opcion == "3":
            jugador.mover("a")
            resultado = evento_random(jugador)

        elif opcion == "4":
            jugador.mover("d")
            resultado = evento_random(jugador)

        elif opcion == "5":
            jugador.inventario.mostrar()

        elif opcion == "6":
            jugador.usar_comida()

        elif opcion == "7":
            jugador.botar_item()

        elif opcion == "8":
            print(f"Puntos: {jugador.puntos}")

        elif opcion == "9":
            print("Saliendo del juego")
            break

        else:
            print("Opcion invalida")

        if resultado == "gano":
            break

        elif resultado == "perdio":
            break

    # RESULTADO FINAL

    print("\n===== RESULTADO FINAL =====")

    if jugador.vida > 0:

        print("GANASTE EL JUEGO")
        resultado = "gano" 

    else:

        print("GAME OVER")
        resultado = "perdio"

    print(f"Puntos finales: {jugador.puntos}")
    print(f"Distancia recorrida: {jugador.distancia_total}")

    guardar_resultado(jugador, resultado)

    mostrar_top5()

    print(f"\nPersonajes creados: {Personaje.total_personajes()}")


if __name__ == '__main__':
    main()
