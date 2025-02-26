from app.services.llm import AIProcessor
from app.utils.functions import obter_prompt
from app.schemas.orthography_request import OrthographyCheckRequest
from app.schemas.orthography_response import OrthographyCheckResponse
from app.schemas.response_formats import OrthographyCheckResponseFormat


ai_processor = AIProcessor()


def check_process(req: OrthographyCheckRequest) -> OrthographyCheckResponse:
    ai_model = req.ai_model
    language = req.language.value
    prompt = obter_prompt(tipo_de_prompt='orthography').format(language)
    text = req.text
    response = ai_processor.process(ai_model, prompt, text, OrthographyCheckResponseFormat)
    return OrthographyCheckResponse(**response)
