
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from ai_ops.core.config import settings


COLLECTION_NAME = "ai_ops_documents"
SOURCE_FILE = "Resume_BDHM.pdf"
MAX_DISTANCE = 0.55
RESULT_COUNT = 2


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
        collection_name=COLLECTION_NAME,
        distance_strategy="cosine",
    )

    question = input("Ask a question about your documents: ").strip()

    if not question:
        print("Please enter a question.")
        return

    results = vector_store.similarity_search_with_score(
        question,
        k=RESULT_COUNT,
        filter={"source": SOURCE_FILE},
    )

    # Lower cosine distance indicates a closer match.
    relevant_results = [
        (document, distance)
        for document, distance in results
        if distance <= MAX_DISTANCE
    ]

    if not relevant_results:
        print(
            "No sufficiently relevant matches found. "
            "Try rephrasing your question."
        )
        return

    print(f"\nQuestion: {question}\n")

    for document, distance in relevant_results:
        print(f"Source: {document.metadata.get('source', 'Unknown')}")
        print(f"Page: {document.metadata.get('page', 'Unknown')}")
        print(f"Distance: {distance:.4f}")
        print(f"Text: {document.page_content}")
        print("-" * 50)


if __name__ == "__main__":
    main()
