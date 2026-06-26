from rag import crear_retriever

print("Creando retriever...")

retriever = crear_retriever()

print("Retriever creado correctamente.")

pregunta = input("\nHaz una pregunta: ")

documentos = retriever.invoke(pregunta)

print("\n===== DOCUMENTOS RECUPERADOS =====\n")

for i, doc in enumerate(documentos, start=1):
    print(f"Documento {i}")
    print(doc.page_content)
    print("-" * 40)