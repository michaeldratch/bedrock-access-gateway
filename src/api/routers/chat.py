from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse

from api.auth import api_key_auth
from api.models.bedrock import BedrockAgentModel, BedrockModel
from api.schema import ChatRequest, ChatResponse, ChatStreamResponse, Error
from api.setting import DEFAULT_MODEL

router = APIRouter(
    prefix="/chat",
    dependencies=[Depends(api_key_auth)],
    # responses={404: {"description": "Not found"}},
)


@router.post(
    "/completions", response_model=ChatResponse | ChatStreamResponse | Error, response_model_exclude_unset=True
)
async def chat_completions(
    chat_request: Annotated[
        ChatRequest,
        Body(
            examples=[
                {
                    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello!"},
                    ],
                }
            ],
        ),
    ],
):
    if chat_request.model.lower().startswith("gpt-"):
        chat_request.model = DEFAULT_MODEL

    # Route to the appropriate model implementation.
    # Exception will be raised if model not supported.
    if chat_request.model.startswith("bedrock-agent:"):
        model = BedrockAgentModel()
    else:
        model = BedrockModel()
    model.validate(chat_request)
    if chat_request.stream:
        return StreamingResponse(content=model.chat_stream(chat_request), media_type="text/event-stream")
    return await model.chat(chat_request)
