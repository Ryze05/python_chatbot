from typing import Iterator

from openai import APIConnectionError, APIStatusError, OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam


class OllamaClient:
    client: OpenAI
    messages: list[ChatCompletionMessageParam]
    model: str
    max_context: int

    def __init__(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        max_context: int = 8,
        url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
    ) -> None:
        self.model = model
        self.client = OpenAI(base_url=url, api_key=api_key)
        self.messages = messages
        self.max_context = max_context

    def window_context(self) -> list[ChatCompletionMessageParam]:
        if len(self.messages) <= self.max_context + 1:
            return self.messages

        system_msg = self.messages[0]
        messages = self.messages[1:]
        return [system_msg] + messages[-self.max_context:]

    def ask_ia(self, prompt: str) -> Iterator[str]:
        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        context = self.window_context()

        try:
            response_ai = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                max_completion_tokens=150,
                messages=context,
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

    def clear_context(self) -> None:
        self.messages = [self.messages[0]]

    def full_history(self) -> list[ChatCompletionMessageParam]:
        return self.messages[1:]
