from fastapi import APIRouter
from models.models import QaConfig
from rag_utils.initializer import chatbot


router = APIRouter()

@router.post("/apiservice/query")
def naswer_info(user_input: QaConfig):

    answer = chatbot.conversational_chat(user_input.query)
    return {"answer": answer}

