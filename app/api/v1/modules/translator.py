from app.services.llm import AIProcessor
from app.utils.functions import obter_prompt
from app.schemas.translator_response import TranslateTextResponse
from app.schemas.translator_request import TranslateTextRequest
from app.schemas.response_formats import TranslateResponseFormat

ai_processor = AIProcessor()


def translate_process(req: TranslateTextRequest) -> TranslateTextResponse:
    ai_model = req.ai_model
    in_lang = req.language_in.value
    out_lang = req.language_out.value
    prompt = obter_prompt(tipo_de_prompt='translate').format(in_lang, out_lang)
    text = req.text
    response = ai_processor.process(ai_model, prompt, text, TranslateResponseFormat)
    return TranslateTextResponse(**response)
