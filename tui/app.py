# tui/app.py
from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from rag.retriever import answer

class WikiTUI(App):
    CSS = "Screen { padding: 1; }"

    def compose(self) -> ComposeResult:
        yield Static("📚 Wiki Assistant (Ollama)")
        yield Input(placeholder="Ask a question…", id="query")
        yield Static("", id="output")

    async def on_input_submitted(self, event: Input.Submitted):
        query = event.value
        output = self.query_one("#output", Static)
        output.update("Thinking…")

        try:
            response = answer(query)
            output.update(response)
        except Exception as e:
            output.update(str(e))

if __name__ == "__main__":
    WikiTUI().run()
