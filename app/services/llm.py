from typing import Type, TypeVar
from pydantic import BaseModel

from app.services.openai.chatgpt import ChatGPT
from app.services.google.gemini import Gemini
from app.models.ai_model import AIModelEnum


T = TypeVar('T', bound=BaseModel)


class AIProcessor:
    def __init__(self):
        pass

    def chat_gpt_parsed_response(self, prompt: str, text: str, response_format: T) -> T:
        chat_gpt = ChatGPT(prompt, text, response_format)
        response = chat_gpt.parsed_response()
        return response

    def gemini_parsed_response(self, prompt: str, text: str, response_format: T) -> T:
        gemini = Gemini(prompt, text, response_format)
        response = gemini.parsed_response()
        return response

    def process(self, ai_model: AIModelEnum, prompt: str, text: str, response_format: T) -> T:
        print(f"model: {ai_model.value}")
        combined_data = {}
        combined_data["ai_model"] = ai_model.value
        if ai_model == AIModelEnum.CHATGPT:
            print("chatgpt")
            model_response = self.chat_gpt_parsed_response(prompt, text, response_format)
        elif ai_model == AIModelEnum.GEMINI:
            print("gemini")
            model_response = self.gemini_parsed_response(prompt, text, response_format)
        else:
            raise ValueError(f"Modelo de IA não suportado: {ai_model}")
        if isinstance(model_response, BaseModel):
            dump_response = model_response.model_dump()
        else:
            raise TypeError("model_response não é um objeto BaseModel.")
        combined_data.update(**dump_response)
        print(f"data: {combined_data}")
        return response_format(**combined_data)