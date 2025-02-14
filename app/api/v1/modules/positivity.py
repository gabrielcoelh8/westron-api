from app.services.openai.chatgpt import ChatGPT
from app.utils.functions import obter_prompt
from app.schemas.response_formats import IsPositiveResponseFormat, ToPositiveResponseFormat
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest


def is_positive_text_process(req: IsPositiveRequest) -> IsPositiveResponseFormat:
    text = req.text
    prompt = obter_prompt(tipo_de_prompt='is_positive')
    chat_gpt = ChatGPT(prompt, text, response_format=IsPositiveResponseFormat)
    response = chat_gpt.get_parsed_response()
    return response

def to_positive_text_process(req: ToPositiveRequest) -> ToPositiveResponseFormat:
    text = req.text
    prompt = obter_prompt(tipo_de_prompt='to_positive')
    chat_gpt = ChatGPT(prompt, text, response_format=ToPositiveResponseFormat)
    response = chat_gpt.get_parsed_response()
    return response