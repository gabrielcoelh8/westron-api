from app.services.openai.chatgpt import ChatGPT
from app.utils.functions import obter_prompt
from app.schemas.response_formats import TranslateResponseFormat
from app.schemas.translator_response import TranslateFileResponse, TranslateTextResponse
from app.schemas.translator_request import TranslateTextRequest


def translate_process(req: TranslateTextRequest) -> TranslateTextResponse:
    text = req.text
    in_lang = req.language_in
    out_lang = req.language_out
    prompt = obter_prompt(tipo_de_prompt='translate').format(in_lang, out_lang)
    chat_gpt = ChatGPT(prompt, text, response_format=TranslateResponseFormat)
    response = chat_gpt.get_parsed_response()
    return response

def translate_file_process(req: TranslateTextRequest) -> TranslateFileResponse:
    # TODO: PNG/JPG to Text
    text = req.text
    in_lang = req.language_in
    out_lang = req.language_out
    prompt = obter_prompt(tipo_de_prompt='translate').format(in_lang, out_lang)
    chat_gpt = ChatGPT(prompt, text, response_format=TranslateResponseFormat)
    response = chat_gpt.get_parsed_response()
    return response