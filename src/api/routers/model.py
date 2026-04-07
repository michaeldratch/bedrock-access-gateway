from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from api.auth import api_key_auth
from api.models.bedrock import BedrockAgentModel, BedrockModel
from api.schema import Model, Models
from api.setting import ENABLE_BEDROCK_AGENTS

router = APIRouter(
    prefix="/models",
    dependencies=[Depends(api_key_auth)],
    # responses={404: {"description": "Not found"}},
)

chat_model = BedrockModel()
agent_model = BedrockAgentModel()


def _all_model_ids() -> list[str]:
    ids = chat_model.list_models()
    if ENABLE_BEDROCK_AGENTS:
        ids = ids + agent_model.list_models()
    return ids


async def validate_model_id(model_id: str):
    if model_id not in _all_model_ids():
        raise HTTPException(status_code=500, detail="Unsupported Model Id")


@router.get("", response_model=Models)
async def list_models():
    model_list = [Model(id=model_id) for model_id in _all_model_ids()]
    return Models(data=model_list)


@router.get(
    "/{model_id}",
    response_model=Model,
)
async def get_model(
    model_id: Annotated[
        str,
        Path(description="Model ID", example="anthropic.claude-3-sonnet-20240229-v1:0"),
    ],
):
    await validate_model_id(model_id)
    return Model(id=model_id)
