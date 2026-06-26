from agente import agent

print("=" * 50)
print("AGENTE IA + GEMINI + RAG + MEMORY")
print("=" * 50)

while True:

    pregunta = input("\nTú: ")

    if pregunta.lower() == "salir":
        print("\nHasta luego.")
        break

    respuesta = agent.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": pregunta
                }
            ]
        },

        config={
            "configurable": {
                "thread_id": "jonathan"
            }
        }

    )

    print("\nAgente:\n")

    ultimo = respuesta["messages"][-1].content

    if isinstance(ultimo, list):
        print(ultimo[0]["text"])
    else:
        print(ultimo)