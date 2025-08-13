import gradio as gr
from pathlib import Path
from adamic.bible import Bible
from adamic.ai import stream_ai_response
from adamic.logic.database import Database
from adamic.logic.xp_manager import XPManager
from adamic.logic.leaderboard import PAGE_SIZE, top_users

# Load the Bible data
data_path = Path(__file__).parent / "adamic" / "data" / "sample_bible.json"
bible = Bible(data_path)

# XP management
db_path = Path(__file__).parent / "xp.db"
database = Database(db_path)
xp_manager = XPManager(database)
USER_ID = "default"


def _format_passage(book, chapter, verse):
    return f"{book} {int(chapter)}:{int(verse)}"


def view_verse(book, chapter, verse):
    passage = _format_passage(book, chapter, verse)
    text = bible.get_verse(book, chapter, verse)
    xp = xp_manager.award_verse_view(USER_ID, passage)
    avg = database.get_average_rating(passage)
    return text, xp, avg


def rate_passage(book, chapter, verse, rating):
    passage = _format_passage(book, chapter, verse)
    avg, xp = xp_manager.submit_rating(USER_ID, passage, int(rating))
    return avg, xp

def search_bible(keyword):
    results = bible.search(keyword)
    return "\n".join(results) if results else "No results found."

def ai_query(question, timeout):
    accumulated = ""
    for chunk in stream_ai_response(question, timeout=timeout):
        accumulated += chunk
        yield accumulated


def load_leaderboard(period: str, page: int):
    page = int(page)
    rows = top_users(database, page=page, period=period)
    return [
        [idx + 1 + (page - 1) * PAGE_SIZE, user_id, points]
        for idx, (user_id, points) in enumerate(rows)
    ]

with gr.Blocks() as demo:
    gr.Markdown("# Adamic Bible Reader")

    with gr.Tab("Reader"):
        gr.Markdown("### Verse Lookup")
        with gr.Row():
            book_dropdown = gr.Dropdown(bible.get_books(), label="Book")
            chapter_input = gr.Number(label="Chapter", precision=0)
            verse_input = gr.Number(label="Verse", precision=0)
        output_text = gr.Textbox(label="Verse Text")
        xp_display = gr.Number(label="Current XP", value=xp_manager.get_xp(USER_ID), interactive=False)
        avg_display = gr.Number(label="Average Rating", value=0, interactive=False)
        load_button = gr.Button("Load Verse")
        load_button.click(
            view_verse,
            inputs=[book_dropdown, chapter_input, verse_input],
            outputs=[output_text, xp_display, avg_display],
        )
        rating_slider = gr.Slider(1, 5, step=1, label="Your Rating")
        rate_button = gr.Button("Submit Rating")
        rate_button.click(
            rate_passage,
            inputs=[book_dropdown, chapter_input, verse_input, rating_slider],
            outputs=[avg_display, xp_display],
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

    with gr.Tab("Leaderboard"):
        period_radio = gr.Radio(
            ["all-time", "weekly"], label="Period", value="all-time"
        )
        page_number = gr.Number(label="Page", value=1, precision=0, minimum=1)
        load_button = gr.Button("Load")
        leaderboard_table = gr.Dataframe(
            headers=["Rank", "User", "XP"], interactive=False
        )
        load_button.click(
            load_leaderboard,
            inputs=[period_radio, page_number],
            outputs=leaderboard_table,
        )

if __name__ == "__main__":
    demo.launch()
