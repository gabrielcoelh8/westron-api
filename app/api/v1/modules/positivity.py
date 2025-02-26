from app.services.llm import AIProcessor
from app.utils.functions import obter_prompt
from app.schemas.positivity_response import IsPositiveResponse, ToPositiveResponse
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest
from app.schemas.response_formats import IsPositiveResponseFormat, ToPositiveResponseFormat


ai_processor = AIProcessor()


def is_positive_text_process(req: IsPositiveRequest) -> IsPositiveResponse:
    ai_model = req.ai_model
    prompt = obter_prompt(tipo_de_prompt='is_positive')
    text = req.text
    response = ai_processor.process(ai_model, prompt, text, IsPositiveResponseFormat)
    return IsPositiveResponse(**response)


def to_positive_text_process(req: ToPositiveRequest) -> ToPositiveResponse:
    ai_model = req.ai_model
    prompt = obter_prompt(tipo_de_prompt='to_positive')
    text = req.text
    response = ai_processor.process(ai_model, prompt, text, ToPositiveResponseFormat)
    return ToPositiveResponse(**response)
