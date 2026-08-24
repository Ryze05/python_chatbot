from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class OllamaClient:
    client: OpenAI
    messages: list[ChatCompletionMessageParam]
    model: str

    def __init__(
        self,
        model: str,
        url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
    ) -> None:
        self.model = model
        self.client = OpenAI(base_url=url, api_key=api_key)
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Eres un profesor de matemáticas. "
                    "Responde únicamente preguntas de matemáticas. Si "
                    "la pregunta no es de matemáticas, responde exactamente: "
                    "Lo sentimos, este modelo solo responde "
                    "a preguntas de mates"
                ),
            },
            {"role": "user", "content": "Quien descubrió américa"},
            {
                "role": "assistant",
                "content": (
                    "Lo sentimos, este modelo solo responde "
                    "a preguntas de mates"
                ),
            },
            {"role": "user", "content": "Calcula cuanto es 25*4"},
            {
                "role": "assistant",
                "content": "El resultado de 25 * 4 es 100.",
            },
        ]

    def ask_ia(self, prompt: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        response_ia = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            max_completion_tokens=150,
            messages=self.messages,
        )

        return response_ia.choices[0].message.content or ""
