
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_ops.agent import build_agent

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class AskResponse(BaseModel):
    question: str
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        agent = build_agent()

        result = agent.invoke({
            "messages": [
                {"role": "user", "content": request.question}
            ]
        })

        answer = next(
            (
                message.content
                for message in reversed(result["messages"])
                if getattr(message, "type", None) == "ai"
                and isinstance(message.content, str)
                and message.content.strip()
            ),
            None,
        )

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The AI assistant did not return a text answer.",
            )

        return AskResponse(
            question=request.question,
            answer=answer,
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="The AI assistant is unavailable. Check that Ollama is running and the model is installed.",
        )
