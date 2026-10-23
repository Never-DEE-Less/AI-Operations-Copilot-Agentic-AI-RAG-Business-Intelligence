
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

from ai_ops.core.config import settings


def main():
    connection = (
        f"postgresql+psycopg://{settings.postgres_user}:"
        f"{settings.postgres_password}@{settings.postgres_host}:"
        f"{settings.postgres_port}/{settings.postgres_db}"
    )

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = PGVector(
        embeddings=embeddings,
        connection=connection,
        embedding_length=768,
        collection_name="ai_ops_documents",
        distance_strategy="cosine",
       
    )

    documents = [
        Document(
            page_content=(
                "The Services category generated €441,350 in revenue."
            ),
            metadata={
                "source": "sample_business_report",
                "category": "Services",
            },
        ),
        Document(
            page_content=(
                "The Hardware category generated €419,882 in revenue."
            ),
            metadata={
                "source": "sample_business_report",
                "category": "Hardware",
            },
        ),
        Document(
            page_content=(
                "The company sells cloud services and security products."
            ),
            metadata={
                "source": "sample_business_report",
                "category": "General",
            },
        ),
    ]

    vector_store.add_documents(documents)

    question = "What are the main concepts explained in this document?"

    results = vector_store.similarity_search_with_score(
        question,
        k=2,
    )

    print(f"\nQuestion: {question}\n")

    for document, score in results:
        print(f"Text: {document.page_content}")
        print(f"Metadata: {document.metadata}")
        print(f"Distance: {score:.4f}\n")


if __name__ == "__main__":
    main()
