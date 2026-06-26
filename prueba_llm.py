from llm import llm

respuesta = llm.invoke("Hola, preséntate en una sola oración.")

print(respuesta.content)