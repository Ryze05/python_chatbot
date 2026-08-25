from typing import Iterator

from openai import APIConnectionError, APIStatusError, OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam


class OllamaClient:
    client: OpenAI
    messages: list[ChatCompletionMessageParam]
    model: str

    def __init__(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
    ) -> None:
        self.model = model
        self.client = OpenAI(base_url=url, api_key=api_key)
        self.messages = messages

    def ask_ia(self, prompt: str) -> Iterator[str]:
        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        try:
            response_ai = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                max_completion_tokens=150,
                messages=self.messages,
                stream=True,
            )

            response_str = ""
            for chunk in response_ai:
                token = chunk.choices[0].delta.content or ""
                response_str += token
                yield token

            self.messages.append(
                {
                    "role": "assistant",
                    "content": response_str
                }
            )
        except APIConnectionError:
            self.messages.pop()
            yield "❌ Error: No se pudo establecer conexión con el proveedor."

        except APIStatusError as e:
            self.messages.pop()
            yield f"❌ Error del servicio ({e.status_code}): {e.message}"

        except OpenAIError as e:
            self.messages.pop()
            yield f"❌ Error inesperado de la API: {e}"
