from ollama_practice.ollama_client import OllamaClient


def main() -> None:
    user_prompt = input("Que necesitas:\n")
    client = OllamaClient("llama3.2")
    print(client.ask_ia(user_prompt))


if __name__ == "__main__":
    main()
