from ollama_practice.ollama_client import OllamaClient
from openai.types.chat import ChatCompletionMessageParam


def main() -> None:
    messages: list[ChatCompletionMessageParam] = [
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
        }
    ]

    client_ai = OllamaClient("llama3.2", messages)

    while True:
        input_str = (
            "Dime que es lo que necesitas, "
            "usa 0 para salir:\n"
        )
        user_input: str = input(input_str)
        if user_input == "0":
            break
        response_ai = (
            "Chat:\n"
            f"\t{client_ai.ask_ia(user_input)}"
        )
        print(response_ai)


if __name__ == "__main__":
    main()
