
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from ai_ops.core.config import settings


COLLECTION_NAME = "ai_ops_documents"
SOURCE_FILE = "Resume_BDHM.pdf"

# Lower cosine distance means a closer match.
MAX_DISTANCE = 0.50
RESULT_COUNT = 2


def search_resume(question: str) -> list[dict]:
    """Retrieve the closest relevant chunks from the indexed resume."""

    question = question.strip()
    if not question:
        return []

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

    results = vector_store.similarity_search_with_score(
        question,
        k=RESULT_COUNT,
        filter={"source": SOURCE_FILE},
    )

    relevant_results = [
        (document, distance)
        for document, distance in results
        if distance <= MAX_DISTANCE
    ]

    return [
        {
            "source": document.metadata.get("source", "Unknown"),
            "page": document.metadata.get("page", "Unknown"),
            "text": document.page_content,
            "distance": round(float(distance), 4),
        }
        for document, distance in relevant_results
    ]
