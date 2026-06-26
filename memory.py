import os

ARCHIVO = os.path.join(os.path.dirname(__file__), "memory.txt")


def guardar(texto):
    """Agrega un recuerdo al final de memory.txt."""

    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(texto.strip() + "\n")


def leer():
    """Lee todos los recuerdos almacenados en memory.txt."""

    if not os.path.exists(ARCHIVO):
        return ""

    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return f.read().strip()


def limpiar():
    """Borra todo el contenido de memory.txt."""

    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write("")