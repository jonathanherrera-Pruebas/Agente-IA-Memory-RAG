from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

RUTA_DOCUMENTOS = "documentos"
RUTA_CHROMA = "chroma_db"


def crear_retriever():

    loader = DirectoryLoader(
        RUTA_DOCUMENTOS,
        glob="*.txt",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )

    documentos = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=documentos,
        embedding=embeddings,
        persist_directory=RUTA_CHROMA
    )

    return db.as_retriever(search_kwargs={"k": 2})


retriever = crear_retriever()