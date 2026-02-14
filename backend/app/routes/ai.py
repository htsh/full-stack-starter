from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import current_active_user
from app.models.user import User
from app.services.ai import run_ai_task
from app.services.credits import deduct_credits

router = APIRouter(prefix="/ai", tags=["ai"])

AI_COST_PER_REQUEST = 1


class AIRequest(BaseModel):
    prompt: str


class AIResponse(BaseModel):
    result: str
    credits_remaining: int


@router.post("/generate", response_model=AIResponse)
async def generate(
    body: AIRequest,
    user: User = Depends(current_active_user),
):
    if user.credits < AI_COST_PER_REQUEST:
        raise HTTPException(status_code=402, detail="Insufficient credits")

    result = await run_ai_task(body.prompt)
    user = await deduct_credits(user, AI_COST_PER_REQUEST)

    return AIResponse(result=result, credits_remaining=user.credits)
