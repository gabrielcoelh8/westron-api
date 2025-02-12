from os import environ
from time import time
from typing import Any

from openai import AzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.services.chat_gpt.endpoint import Endpoint
from app.services.chat_gpt.model import Model
from app.services.chat_gpt.utils import count_tokens


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

    def __init__(self, prompt: str, text: str, response_format: Any = None):
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

    def _create_client(self) -> AzureOpenAI:
        api_version = environ.get('AZURE_OPENAI_API_VERSION')
        client = AzureOpenAI(
            azure_endpoint=self._model.endpoint.url,
            api_key=self._model.endpoint.key,
            api_version=api_version
        )
        return client

    def _create_completion(self) -> ChatCompletion:
        max_tokens = (
            self._model.output_size - self._estimated_output_size - self._input_size
            if self._model.input_size == self._model.output_size else self._model.output_size
        )

        self._start = time()
        if self._response_format:
            completion = self._client.beta.chat.completions.parse(
                model=self._model.name,
                messages=self._messages,
                temperature=0,
                max_tokens=max_tokens,
                top_p=0,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                seed=0,
                response_format=self._response_format,  # Passa o modelo Pydantic para obter saída estruturada
            )
        else:
            completion = self._client.chat.completions.create(
                model=self._model.name,
                messages=self._messages,
                temperature=0,
                max_tokens=max_tokens,
                top_p=0,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                seed=0,
            )

        self._end = time()
        self._set_time_to_completion()

        if completion.choices[0].finish_reason == 'length':  # TODO: adicionar time_out aqui também
            self._model.ignore = True
            self._model = self._select_model()
            completion = self._create_completion()

        return completion

    def _create_messages(self) -> list[dict]:
        messages = [
            {'role': 'system', 'content': self._prompt},
            {'role': 'user', 'content': [{'type': 'text', 'text': self._text}]}
        ]
        return messages

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
        # lista modelos a serem ignorados
        models_to_ignore = [model for model in self._models if model.ignore]

        # lista tamanhos de entradas e saídas a serem ignoradas
        inputs_to_ignore = [model.input_size for model in models_to_ignore if model.ignore]
        outputs_to_ignore = [model.output_size for model in models_to_ignore if model.ignore]

        # lista modelos cujo atributo ignore possui valor falso
        models = [model for model in self._models if not model.ignore]

        # lista modelos cujos tamanhos de entrada e saída não estão nas listas de tamanhos a serem ignorados
        models = [
            model for model in models
            if model.input_size not in inputs_to_ignore and model.output_size not in outputs_to_ignore
        ]

        # lista os modelos que provavelmente suportam a entrada
        models = [model for model in models if model.input_size >= self._input_size]

        # lista os modelos que provavelmente suportam a saida
        models = [
            model for model in models if any([
                model.input_size != model.output_size and model.output_size >= self._estimated_output_size,
                model.input_size == model.output_size and model.output_size >= (
                        self._input_size + self._estimated_output_size
                )
            ])
        ]

        # ordena os modelos por tamanho de entrada, tamanho de saida e tempo de resposta
        models.sort(key=lambda model: (model.input_size, model.output_size, model.time))

        return models[0]

    def _set_time_to_completion(self) -> None:
        time_to_completion = self._end - self._start
        self._model.time = self._model.time + time_to_completion

    def get_completion(self) -> ChatCompletion:
        return self._completion

    def get_response(self) -> str:
        return self._completion.choices[0].message.content

    def get_parsed_response(self):
        response_parsed = self._completion.choices[0].message.parsed
        return response_parsed.model_dump()
