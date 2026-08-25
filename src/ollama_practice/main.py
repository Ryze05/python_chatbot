from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
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
    table.add_row("/save", "Exporta la conversación actual a un archivo .md")
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


def save_history(
    console: Console,
    history: list[ChatCompletionMessageParam]
) -> None:
    if not history:
        console.print("[dim]No hay nada que guardar todavía.[/dim]")
        return

    path_history = Path("src/ollama_practice/history")

    if not path_history.exists():
        path_history.mkdir()

    date_session = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d_%H-%M-%S.%f_UTC"
    )

    file_name = path_history / Path(f"asistente_mates_{date_session}.md")

    data_file = dedent(f"""
                # 👨‍🏫 Sesión con el Profesor de Matemáticas\n
                **fecha:** {datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S.%f_UTC"
                )}
                """).strip()

    for i in history:
        role = i.get("role")
        content = i.get("content") or ""

        if role == "user":
            data_file += f"\n\n## 👤 Usuario\n\n{content}\n"
        elif role == "assistant":
            data_file += f"\n## 🤖 Profesor\n\n{content}\n---"

    file_name.write_text(data_file, "utf-8")
    console.print(
        "[bold green]💾 Historial guardado con éxito en:[/bold green]"
        f"[cyan]{file_name}[/cyan]"
    )


def main() -> None:
    console = Console()

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": (
                "Eres un profesor de matemáticas. "
                "Sigue estas reglas en este orden de prioridad:\n"
                "1. Si el usuario saluda, salúdalo cordialmente y pregúntale "
                "en qué problema de matemáticas necesita ayuda.\n"
                "2. Si el usuario pregunta quién eres, especifica que eres "
                "un profesor de matemáticas.\n"
                "3. Para cualquier otra pregunta, responde únicamente si es "
                "de matemáticas. Si no lo es, responde exactamente: Lo "
                "sentimos este modelo solo responde a preguntas de mates.\n\n"
                "IMPORTANTE SOBRE EL FORMATO:\n"
                "- Responde SIEMPRE estructurando tus explicaciones en "
                "Markdown enriquecido.\n"
                "- Usa títulos (##, ###), negritas para destacar conceptos "
                "clave y listas con viñetas (-) para pasos.\n"
                "- Si muestras fórmulas o código de apoyo, mételos en bloques "
                "de código con sintaxis resaltada (```python ... ```).\n\n"
                "Ejemplos de comportamiento esperado:\n"
                "Usuario: Quien descubrió américa\n"
                "Asistente: Lo sentimos, este modelo solo responde a "
                "preguntas de mates\n\n"
                "Usuario: Calcula cuanto es 25*4\n"
                "Asistente: ## Cálculo de Multiplicación\n\nEl resultado "
                "de **25 × 4** es:\n- **Total:** `100`"
            ),
        },
    ]

    client_ai = OllamaClient("llama3.2", messages)

    showBanner(console)

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]Tú[/bold cyan]").strip()

            if not user_input:
                continue

            command = user_input.lower()

            if command in ("0", "salir", "exit"):
                console.print("[bold cyan]¡Hasta pronto! 👋[/bold cyan]\n")
                break

            if command == "/clear":
                client_ai.clear_context()
                console.print(
                    "[bold green]🧹 Historial reiniciado "
                    "correctamente.[/bold green]"
                )
                continue

            if command == "/history":
                history = client_ai.full_history()
                if not history:
                    console.print(
                        "[dim]No hay mensajes en "
                        "el historial aún.[/dim]"
                    )
                    continue

                console.print(
                    "\n[bold underline]📔 Historial de "
                    "conversación:[/bold underline]\n",
                    justify="center"
                )

                for i in history:
                    role = i.get("role")
                    content = i.get("content") or ""
                    if role == "user":
                        console.print(
                            Panel(
                                renderable=f"{content}",
                                title="👤 Tú",
                                border_style="yellow"
                            )
                        )
                    elif role == "assistant":
                        console.print(
                            Panel(
                                Markdown(f"{content}"),
                                title="🤖 Profesor",
                                border_style="green"
                            )
                        )
                    elif role == "system":
                        continue
                continue

            if command == "/help":
                showHelp(console)
                continue

            if command == "/save":
                save_history(console, client_ai.full_history())
                continue

            console.print("\n[bold green]Profesor:[/bold green]")

            full_response = ""

            with Live(
                Markdown(""),
                refresh_per_second=15,
                console=console
            ) as live:
                for token in client_ai.ask_ia(user_input):
                    full_response += token
                    live.update(Markdown(full_response))
        except KeyboardInterrupt:
            console.print(
                "\n\n[bold red]⚠️  Sesión finalizada con Ctrl+C."
                "¡Hasta la próxima![/bold red]\n"
            )
            break


if __name__ == "__main__":
    main()
