from openai import OpenAI
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

    def ask_ia(self, prompt: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        response_ai = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            max_completion_tokens=150,
            messages=self.messages,
        )

        response_str = response_ai.choices[0].message.content or ""
        self.messages.append(
            {
                "role": "assistant",
                "content": response_str
            }
        )

        return response_str
