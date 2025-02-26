from os import environ
from typing import Type, Optional, Dict, Any
from google.genai import Client
from pydantic import BaseModel


class Gemini:
    def __init__(
      self, 
      prompt: str, 
      text: str, 
      response_format: Type[BaseModel] = None,
      temperature: float = 0.0,
      top_p: float = 0.95,
      top_k: int = 40,
      max_output_tokens: int = 2048,
      candidate_count: int = 1
    ):
      self._response_format = response_format
      self._prompt = prompt
      self._text = text
      self._temperature = temperature
      self._top_p = top_p
      self._top_k = top_k
      self._max_output_tokens = max_output_tokens
      self._candidate_count = candidate_count
      self._client = self._create_client()
      self._completion = self._create_completion()
    
    def _create_client(self) -> Client:
      return Client(api_key=environ.get("GEMINI_KEY"))
    
    def _create_completion(self):
      try:
        response=self._client.models.generate_content(
          model=environ.get("GEMINI_MODEL"),
          contents=[self._prompt, self._text],
          config={
            'response_mime_type': 'application/json',
            'response_schema': self._response_format,
            'temperature': self._temperature,
            'top_p': self._top_p,
            'top_k': self._top_k,
            'max_output_tokens': self._max_output_tokens,
            'candidate_count': self._candidate_count
          },
        )
        return response
      except Exception as e:
        error_msg = f"Error creating completion with Gemini: {str(e)}"
        raise RuntimeError(error_msg) from e
    
    def parsed_response(self) -> Type[BaseModel]:
        """Retorna o resultado da completion"""
        return self._completion.parsed