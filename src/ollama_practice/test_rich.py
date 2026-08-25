from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

text = Text.from_markup(
    "🤖 [bold green]Asistente de Matemáticas[/bold green] 🤖\n"
    "[dim]Escribe tu consulta o usa [bold blue]/help[/bold blue] "
    "para ver los comandos.[/dim]"
)

text.justify = "center"

panel_banner = Panel.fit(
    text,
    title="Ollama assistant",
    border_style="bold white",
)

console.print(panel_banner)
