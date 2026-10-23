
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from ai_ops.core.config import settings


COLLECTION_NAME = "ai_ops_documents"


def build_vector_store():
    connection = (
        f"postgresql+psycopg://{settings.postgres_user}:"
        f"{settings.postgres_password}@{settings.postgres_host}:"
        f"{settings.postgres_port}/{settings.postgres_db}"
    )

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    return PGVector(
        embeddings=embeddings,
        connection=connection,
        embedding_length=768,
        collection_name=COLLECTION_NAME,
        distance_strategy="cosine",
    )


def ingest_pdf(pdf_path: Path):
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )
    chunks = splitter.split_documents(pages)

    if not chunks:
        raise ValueError(
            "No text could be extracted. The PDF may be scanned or empty."
        )

    for chunk in chunks:
        chunk.metadata["source"] = pdf_path.name

    vector_store = build_vector_store()
    vector_store.add_documents(chunks)

    print(f"PDF: {pdf_path.name}")
    print(f"Pages loaded: {len(pages)}")
    print(f"Chunks stored: {len(chunks)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest a PDF into the AI Ops RAG vector store."
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the PDF file to ingest.",
    )
    args = parser.parse_args()

    ingest_pdf(args.pdf_path)
