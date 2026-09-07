from fastapi import APIRouter, HTTPException, status

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from backend.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)


chat_service = ChatService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):
    try:
        response = chat_service.chat(
            message=request.message,
            thread_id=request.thread_id,
        )

        return ChatResponse(
            thread_id=request.thread_id,
            response=response,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent execution failed.",
        ) from exc