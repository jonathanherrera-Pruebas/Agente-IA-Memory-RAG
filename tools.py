from datetime import datetime
from rag import retriever


# ==========================================
# HORA
# ==========================================

def obtener_hora():

    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ==========================================
# CALCULADORA
# ==========================================

def calculadora(expresion):

    try:

        return str(eval(expresion))

    except Exception:

        return "No pude resolver esa operación."


# ==========================================
# RAG
# ==========================================

def buscar_documentos(pregunta):

    docs = retriever.invoke(pregunta)

    if not docs:

        return None

    return "\n\n".join(doc.page_content for doc in docs)