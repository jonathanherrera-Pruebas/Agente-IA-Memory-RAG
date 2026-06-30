# 🤖 Agente IA Local con Memory, Tools y RAG

Proyecto desarrollado con **Python**, **LangChain**, **Ollama** y **Qwen 2.5:3B**.

El agente funciona completamente de manera local y es capaz de:

- Mantener memoria del usuario.
- Utilizar herramientas (Tools).
- Consultar una base documental mediante RAG.
- Responder preguntas en lenguaje natural mediante un modelo LLM ejecutado con Ollama.

---

# Características

✅ Agente IA local

✅ Memory

✅ Tool: Calculadora

✅ Tool: Fecha y Hora

✅ RAG con ChromaDB

✅ Interfaz gráfica

✅ Modelo local mediante Ollama

---

# Tecnologías utilizadas

- Python 3
- LangChain
- Ollama
- Qwen 2.5:3B
- ChromaDB
- HuggingFace Embeddings
- CustomTkinter

---

# Arquitectura

```
                Usuario
                    │
                    ▼
                Agente IA
                    │
        ┌───────────┼───────────┐
        │           │           │
     Memory       Tools        RAG
        │           │           │
        ▼           ▼           ▼
   Recuerdos   Hora / Cálculo  Documentos
                    │
                    ▼
                 Respuesta
```

---

# Flujo del agente

El agente sigue el siguiente flujo de ejecución:

1. Detecta si el mensaje es una operación matemática.
   - Utiliza la herramienta Calculadora.

2. Detecta si el usuario solicita la hora o la fecha.
   - Utiliza la herramienta Hora.

3. Si el mensaje es una pregunta:
   - Consulta la memoria.
   - Si no encuentra respuesta, consulta el RAG.
   - Si tampoco encuentra información, responde mediante Qwen.

4. Si el mensaje no es una pregunta:
   - Evalúa si la información debe guardarse en la memoria.
   - Si es información importante del usuario, la almacena.
   - En caso contrario continúa como conversación normal.

---

# Estructura del proyecto

```
S2-D4 Agente
│
├── agente.py
├── interfaz.py
├── llm.py
├── memory.py
├── memory.txt
├── rag.py
├── tools.py
├── documentos/
├── chroma_db/
├── requirements.txt
└── README.md
```

---

# Funcionalidades

## Memory

El agente puede recordar información importante del usuario.

Ejemplo:

Usuario:

```
Me llamo Jonathan.
```

Posteriormente:

```
¿Cómo me llamo?
```

Respuesta:

```
Te llamas Jonathan.
```

---

## Tool 1 - Calculadora

Ejemplo:

```
250*18
```

Respuesta:

```
4500
```

---

## Tool 2 - Hora

Ejemplo:

```
¿Qué hora es?
```

Respuesta:

```
26/06/2026 15:45:20
```

---

## RAG

El agente consulta documentos almacenados en ChromaDB.

Ejemplo:

```
¿Qué ofrece el spa?
```

Respuesta basada únicamente en la información de los documentos.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

## 3. Activarlo

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 5. Instalar Ollama

https://ollama.com/

---

## Descargar el modelo

```bash
ollama pull qwen2.5:3b
```

---

## Ejecutar Ollama

```bash
ollama serve
```

---

## Ejecutar el proyecto

```bash
python interfaz.py
```

---

# Ejemplos

### Conversación

```
Hola
```

---

### Calculadora

```
250*18
```

---

### Hora

```
¿Qué hora es?
```

---

### Memoria

```
Me llamo Jonathan.
```

```
¿Cómo me llamo?
```

---

### RAG

```
¿Qué ofrece el spa?
```

---

# Autor

Jonathan David Herrera García

---

# Licencia

Proyecto desarrollado con fines académicos.

## Actualización de prueba3 del pipeline CI/CD