import re

from llm import llm
from memory import guardar, leer
from tools import buscar_documentos, calculadora, obtener_hora


class Mensaje:
    """Objeto simple con atributo .content para compatibilidad con la interfaz."""

    def __init__(self, texto):
        self.content = texto


class AgenteLocal:
    """
    Asistente IA completamente local.

    Flujo secuencial controlado por Python:
    1. Calculadora       (regex)
    2. Hora / Fecha      (palabras clave)
    3. Memory            (solo si es pregunta)
    4. RAG               (solo si es pregunta y memory no respondió)
    5. Guardar memoria   (solo si NO es pregunta, Qwen decide SI/NO)
    6. Chat normal       (fallback)
    """

    def __init__(self):
        self.historial = []

    # ==================================================
    # PUNTO DE ENTRADA — compatible con interfaz.py
    # ==================================================

    def invoke(self, datos, config=None):
        """Recibe el formato {"messages": [{"role":"user","content":"..."}]}."""

        pregunta = datos["messages"][-1]["content"]

        # ---- PASO 1: Calculadora ----
        if self._es_operacion_matematica(pregunta):
            return self._usar_calculadora(pregunta)

        # ---- PASO 2: Hora / Fecha ----
        if self._es_pregunta_hora(pregunta):
            return self._usar_hora()

        # ---- PASO 3 y 4: Si es pregunta → Memory → RAG ----
        if self._es_pregunta(pregunta):

            # PASO 3: Memory
            respuesta_memoria = self._intentar_memoria(pregunta)
            if respuesta_memoria is not None:
                return respuesta_memoria

            # PASO 4: RAG
            respuesta_rag = self._intentar_rag(pregunta)
            if respuesta_rag is not None:
                return respuesta_rag

        else:
            # ---- PASO 5: No es pregunta → ¿Guardar en memoria? ----
            if self._debe_guardar(pregunta):
                guardar(pregunta)
                return self._respuesta("Perfecto, lo recordaré.")

        # ---- PASO 6: Conversación normal ----
        return self._chat(pregunta)

    # ==================================================
    # DETECCIÓN — ¿Es una pregunta?
    # ==================================================

    def _es_pregunta(self, texto):
        """Detecta si el mensaje del usuario es una pregunta."""
        limpio = texto.strip().lower()

        # Signos de interrogación
        if "?" in limpio or "¿" in limpio:
            return True

        # Primeras palabras típicas de preguntas en español
        primera = limpio.split()[0] if limpio else ""
        palabras_pregunta = [
            "qué", "que", "quién", "quien", "cómo", "como",
            "cuándo", "cuando", "dónde", "donde", "cuál", "cual",
            "cuánto", "cuanto", "cuántos", "cuantos", "cuántas", "cuantas",
            "sabes", "recuerdas", "conoces", "tienes",
            "dime", "cuéntame", "cuentame", "explícame", "explicame",
        ]
        return primera in palabras_pregunta

    # ==================================================
    # PASO 1 — CALCULADORA (detección por regex)
    # ==================================================

    def _es_operacion_matematica(self, texto):
        """Detecta si el texto es una operación matemática pura."""
        limpio = texto.strip()
        return bool(re.fullmatch(r"[\d\s\+\-\*\/\.\(\)\%\^]+", limpio))

    def _usar_calculadora(self, pregunta):
        expresion = pregunta.strip().replace("^", "**")
        resultado = calculadora(expresion)
        return self._respuesta(resultado)

    # ==================================================
    # PASO 2 — HORA / FECHA (detección por palabras clave)
    # ==================================================

    def _es_pregunta_hora(self, texto):
        """Detecta si el usuario pregunta por la hora o la fecha."""
        palabras = texto.lower()
        claves = [
            "qué hora", "que hora", "hora actual",
            "qué fecha", "que fecha", "fecha actual",
            "día es hoy", "dia es hoy", "qué día", "que dia",
        ]
        return any(c in palabras for c in claves)

    def _usar_hora(self):
        return self._respuesta(obtener_hora())

    # ==================================================
    # PASO 3 — MEMORIA
    # ==================================================

    def _intentar_memoria(self, pregunta):
        """
        Lee memory.txt y le pide a Qwen que responda usando los recuerdos.
        Devuelve la respuesta o None si no encontró información.
        """
        recuerdos = leer()

        if not recuerdos:
            return None

        prompt = f"""Estos son los recuerdos del usuario.

{recuerdos}

Pregunta:
{pregunta}

Responde utilizando únicamente los recuerdos.
Si la respuesta no aparece en los recuerdos responde exactamente: NO_ENCONTRADO"""

        respuesta = llm.invoke(prompt)
        texto = respuesta.content.strip()

        if "NO_ENCONTRADO" in texto:
            return None

        return self._respuesta(texto)

    # ==================================================
    # PASO 4 — RAG
    # ==================================================

    def _intentar_rag(self, pregunta):
        """
        Busca en ChromaDB. Si encuentra contexto relevante, responde.
        Devuelve la respuesta o None si no encontró información.
        """
        contexto = buscar_documentos(pregunta)

        if not contexto:
            return None

        prompt = f"""Contexto:
{contexto}

Pregunta:
{pregunta}

Responde utilizando únicamente el contexto.
Si el contexto no contiene la respuesta responde exactamente: NO_ENCONTRADO"""

        respuesta = llm.invoke(prompt)
        texto = respuesta.content.strip()

        if "NO_ENCONTRADO" in texto:
            return None

        return self._respuesta(texto)

    # ==================================================
    # PASO 5 — ¿GUARDAR EN MEMORIA?
    # ==================================================

    def _debe_guardar(self, pregunta):
        """Le pregunta a Qwen si el mensaje contiene información importante."""

        prompt = f"""Analiza el siguiente mensaje del usuario.

Responde SI cuando el mensaje contenga un dato personal estable como:
- nombre, edad, cumpleaños, estado civil
- trabajo, empresa, profesión, puesto
- escuela, universidad, carrera
- ciudad, país, donde vive
- mascota, nombre de mascota
- comida favorita, color favorito, gustos, hobbies
- datos familiares
- cualquier dato personal que sea útil recordar

Responde NO cuando el mensaje sea:
- un saludo o despedida (hola, adiós, gracias)
- una pregunta
- una operación matemática
- una conversación casual u opinión temporal

Ejemplos:
"Trabajo en SIT Digital." → SI
"Estudio Ingeniería." → SI
"Mi perro se llama Bruno." → SI
"Mi comida favorita es la pizza." → SI
"Vivo en Monterrey." → SI
"Hola." → NO
"Gracias." → NO
"¿Qué hora es?" → NO
"250*18" → NO

Mensaje: "{pregunta}"

Responde ÚNICAMENTE:
SI
o
NO"""

        respuesta = llm.invoke(prompt)
        decision = respuesta.content.strip().upper()

        return "SI" in decision or "SÍ" in decision

    # ==================================================
    # PASO 6 — CHAT NORMAL
    # ==================================================

    def _chat(self, pregunta):
        """Envía directamente el mensaje a Qwen."""
        respuesta = llm.invoke(pregunta)
        return self._respuesta(respuesta.content)

    # ==================================================
    # RESPUESTA — formato compatible con interfaz.py
    # ==================================================

    def _respuesta(self, texto):
        """Devuelve el formato {"messages": [Mensaje(texto)]}."""
        return {
            "messages": [
                Mensaje(str(texto))
            ]
        }


# ==================================================
# INSTANCIA GLOBAL — importada por interfaz.py
# ==================================================

agent = AgenteLocal()