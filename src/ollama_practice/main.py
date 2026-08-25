from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ollama_practice.ollama_client import OllamaClient
from openai.types.chat import ChatCompletionMessageParam


def showHelp(console: Console) -> None:
    table = Table(
        title="📌 Comandos Disponibles",
        border_style="bold white",
        show_lines=True
    )

    table.add_column("Comando", style="bold white", justify="left")
    table.add_column("Descripción", style="bold white", justify="left")

    table.add_row("/clear", "Limpia la memoria y reinicia la conversación")
    table.add_row("/history", "Muestra el historial completo de la sesión")
    table.add_row("/help", "Muestra este menú de ayuda")
    table.add_row("exit", "Cierra el asistente y sale del programa")

    console.print(table)


def showBanner(console: Console) -> None:
    text = Text.from_markup(
        "🤖 [bold green]Asistente de Matemáticas[/bold green] 🤖\n"
        "[dim]Escribe tu consulta o usa [bold blue]/help[/bold blue] "
        "para ver los comandos.[/dim]"
    )

    text.justify = "center"

    console.print(
        Panel.fit(
            text,
            title="Ollama assistant",
            border_style="bold white",
        )
    )


def main() -> None:
    console = Console()

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": (
                "Eres un profesor de matemáticas. "
                "Sigue estas reglas en este orden de prioridad: "
                "1. Si el usuario saluda, salúdalo cordialmente y pregúntale "
                "en qué problema de matemáticas necesita ayuda. "
                "2. Si el usuario pregunta quién eres, cómo te llamas o "
                "qué eres, responde de forma cordial especificando que eres "
                "un profesor de matemáticas. Seguido de eso, pregúntale "
                "en qué problema de matemáticas necesita ayuda. "
                "3. Para cualquier otra pregunta, responde únicamente si es "
                "una pregunta de matemáticas. Si no es una pregunta de "
                "matemáticas, responde exactamente: Lo sentimos, este modelo "
                "solo responde a preguntas de mates"
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

    showBanner(console)

    while True:
        try:
            user_input = input("\nDime que necesitas:\n> ").lower()

            if user_input.strip() in ("0", "salir", "exit"):
                print("Hasta pronto 😁")
                break

            if user_input.strip() == "/clear":
                client_ai.clear_context()
                continue

            if user_input.strip() == "/history":
                history = client_ai.full_history()
                print("\n📔 --- Historial de conversación ---")
                for i in history:
                    role = i.get("role")
                    content = i.get("content") or ""
                    if role == "user":
                        print(f"\n👤 Tú:\n{content}")
                    elif role == "assistant":
                        print(f"\n🤖 Asistente:\n{content}")
                continue

            if user_input.strip() == "/help":
                showHelp(console)
                continue

            print("\nChat:\n", end="", flush=True)

            for token in client_ai.ask_ia(user_input):
                print(token, end="", flush=True)

            print()
        except KeyboardInterrupt:
            print("\n\n⚠️  Sesión cancelada. ¡Hasta pronto!")
            break


if __name__ == "__main__":
    main()
