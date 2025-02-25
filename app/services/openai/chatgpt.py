from os import environ
from time import time
from typing import Any, Type

from openai import NOT_GIVEN, AzureOpenAI, OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from pydantic import BaseModel

from app.services.openai.endpoint import Endpoint
from app.services.openai.model import Model
from app.services.openai.utils import count_tokens


def create_models() -> list[Model]:
    models = list()
    for endpoint, key, models_, inputs, outputs in zip(
            eval(environ.get('GPT_ENDPOINTS')),
            eval(environ.get('GPT_KEYS')),
            eval(environ.get('GPT_MODELS')),
            eval(environ.get('GPT_INPUTS')),
            eval(environ.get('GPT_OUTPUTS'))
    ):
        endpoint = Endpoint(endpoint, key)
        for model, input_, output in zip(models_, inputs, outputs):
            model = Model(model, endpoint, input_, output, 0.0)
            models.append(model)
    return models


class ChatGPT:
    _models = create_models()

    def __init__(self, prompt: str, text: str, response_format: Any = NOT_GIVEN):
        self._response_format = response_format
        self._prompt = prompt
        self._text = text

        self._input_size = self._get_input_size()
        self._estimated_output_size = self._get_estimated_output_size()
        self._model = self._select_model()

        self._messages = self._create_messages()
        self._client = self._create_client()

        self._completion = self._create_completion()
        self._reset_model_ignore()

    def _create_client(self) -> AzureOpenAI | OpenAI:
        if 'openai.azure.com' in self._model.endpoint.url: # for future azure impl.
            api_version = environ.get('AZURE_OPENAI_API_VERSION')
            return AzureOpenAI(
                azure_endpoint=self._model.endpoint.url,
                api_key=self._model.endpoint.key,
                api_version=api_version
            )
        else:
            return OpenAI(
                base_url=self._model.endpoint.url,
                api_key=self._model.endpoint.key,
            )

    def _create_completion(self) -> ChatCompletion:
        max_tokens = (
            self._model.output_size - self._estimated_output_size - self._input_size
            if self._model.input_size == self._model.output_size else self._model.output_size
        )
        
        self._start = time()
        
        try:
            completion_params = {
                "model": self._model.name,
                "messages": self._messages,
                "temperature": 0,
                "max_tokens": max_tokens,
                "top_p": 0,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stop": None,
                "seed": 0,
                "response_format": self._response_format
            }
            completion = self._client.beta.chat.completions.parse(**completion_params)

            self._end = time() 
            self._set_time_to_completion()

            if completion.choices[0].finish_reason == 'length':
                self._model.ignore = True
                self._model = self._select_model()
                completion = self._create_completion()

            return completion

        except Exception as e:
            error_msg = f"Error creating completion with model {self._model.name}: {str(e)}"
            raise RuntimeError(error_msg) from e

    def _create_messages(self) -> list[dict]:
        messages = [
            {'role': 'system', 'content': self._prompt},
            {'role': 'user', 'content': self._text}  # Simplified message format
        ]
        return messages

    # Rest of the class implementation remains the same
    def _get_estimated_output_size(self) -> int:
        estimated_output_size = self._input_size * 0.25
        return round(estimated_output_size)

    def _get_input_size(self) -> int:
        prompt_size = count_tokens(self._prompt)
        text_size = count_tokens(self._text)
        input_size = prompt_size + text_size
        return input_size

    def _reset_model_ignore(self) -> None:
        for model in self._models:
            model.ignore = False

    def _select_model(self) -> Model:
        models_to_ignore = [model for model in self._models if model.ignore]
        inputs_to_ignore = [model.input_size for model in models_to_ignore if model.ignore]
        outputs_to_ignore = [model.output_size for model in models_to_ignore if model.ignore]
        
        models = [model for model in self._models if not model.ignore]
        models = [
            model for model in models
            if model.input_size not in inputs_to_ignore and model.output_size not in outputs_to_ignore
        ]
        
        models = [model for model in models if model.input_size >= self._input_size]
        models = [
            model for model in models if any([
                model.input_size != model.output_size and model.output_size >= self._estimated_output_size,
                model.input_size == model.output_size and model.output_size >= (
                        self._input_size + self._estimated_output_size
                )
            ])
        ]
        
        if not models:
            raise ValueError("No suitable model found for the given input and output requirements")
            
        models.sort(key=lambda model: (model.input_size, model.output_size, model.time))
        return models[0]

    def _set_time_to_completion(self) -> None:
        time_to_completion = self._end - self._start
        self._model.time = self._model.time + time_to_completion

    def get_completion(self) -> ChatCompletion:
        return self._completion

    def response(self) -> str:
        return self._completion.choices[0].message.content

    def parsed_response(self) -> Type[BaseModel]:
        response_parsed = self._completion.choices[0].message.parsed
        return response_parsed.model_dump()