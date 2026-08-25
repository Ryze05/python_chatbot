from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_key: str
    model: str
    max_context: int
    max_tokens: int

    @classmethod
    def from_env(cls) -> "Settings":
        url = os.getenv("OLLAMA_BASE_URL")
        if not url:
            raise ValueError(
                "❌ Falta la variable de entorno obligatoria: OLLAMA_BASE_URL"
            )

        api_key = os.getenv("OLLAMA_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ Falta la variable de entorno obligatoria: OLLAMA_API_KEY"
            )

        model = os.getenv("OLLAMA_MODEL")
        if not model:
            raise ValueError(
                "❌ Falta la variable de entorno obligatoria: OLLAMA_MODEL"
            )

        max_context = os.getenv("OLLAMA_MAX_CONTEXT", "8")

        max_tokens = os.getenv("OLLAMA_MAX_TOKENS", "600")

        return cls(
            base_url=url,
            api_key=api_key,
            model=model,
            max_context=int(max_context),
            max_tokens=int(max_tokens),
        )


settings = Settings.from_env()
