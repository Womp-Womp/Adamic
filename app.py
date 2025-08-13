import gradio as gr
from pathlib import Path
from adamic.bible import Bible
from adamic.config import settings
from adamic.ai import stream_ai_response

# Load the Bible data
data_path = Path(__file__).parent / "adamic" / "data" / "sample_bible.json"
bible = Bible(data_path)

def get_verse_text(book, chapter, verse):
    return bible.get_verse(book, chapter, verse)

def search_bible(keyword):
    results = bible.search(keyword)
    return "\n".join(results) if results else "No results found."

def ai_query(question, timeout):
    accumulated = ""
    for chunk in stream_ai_response(question, timeout=timeout):
        accumulated += chunk
        yield accumulated

with gr.Blocks() as demo:
    gr.Markdown("# Adamic Bible Reader")

    with gr.Tab("Reader"):
        gr.Markdown("### Verse Lookup")
        with gr.Row():
            book_dropdown = gr.Dropdown(bible.get_books(), label="Book")
            chapter_input = gr.Number(label="Chapter", precision=0)
            verse_input = gr.Number(label="Verse", precision=0)
        output_text = gr.Textbox(label="Verse Text")
        load_button = gr.Button("Load Verse")
        load_button.click(
            get_verse_text,
            inputs=[book_dropdown, chapter_input, verse_input],
            outputs=output_text,
        )

        gr.Markdown("---")
        gr.Markdown("### Keyword Search")
        search_input = gr.Textbox(label="Enter keyword")
        search_output = gr.Textbox(label="Search Results")
        search_button = gr.Button("Search")
        search_button.click(
            search_bible,
            inputs=search_input,
            outputs=search_output,
        )

    with gr.Tab("AI Assistant"):
        with gr.Row():
            question_input = gr.Textbox(label="Ask a question")
            timeout_input = gr.Number(
                label="Timeout (s)", value=15, precision=0, minimum=1
            )

        ai_output_text = gr.Textbox(label="AI Response")

        ask_button = gr.Button("Ask")
        cancel_button = gr.Button("Cancel")
        stream = ask_button.click(
            ai_query,
            inputs=[question_input, timeout_input],
            outputs=ai_output_text,
            stream=True,
        )
        cancel_button.click(fn=None, inputs=None, outputs=None, cancels=[stream])

if __name__ == "__main__":
    demo.launch()
