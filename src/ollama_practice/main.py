from openai import OpenAI

URL = "http://localhost:11434/v1"
API_KEY = "ollama"


def call_ai(url: str, api_key: str, prompt: str):
    client_ia = OpenAI(base_url=url, api_key=api_key)
    response = client_ia.chat.completions.create(
        model="llama3.2",
        temperature=0,
        messages=[
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
            {"role": "user", "content": prompt},
        ],
    )
    print(response.choices[0].message.content)


def main() -> None:
    user_prompt = input("Que necesitas:\n")
    call_ai(URL, API_KEY, user_prompt)


if __name__ == "__main__":
    main()
