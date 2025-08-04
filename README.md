# Adamic: AI-Powered Bible Reader

This project is an AI-powered Bible reader designed to provide a modern, accessible, and insightful Bible study tool. It leverages Google's Gemini LLM to offer historical context, various interpretations, cross-references, and more.

## Features

*   **Bible Reader:** A simple interface to read the Bible, with sample data for Genesis and John.
*   **AI Assistant:** A placeholder for an AI assistant that can answer questions about the Bible.
*   **Gradio Interface:** A simple web interface built with Gradio.

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/adamic.git
    cd adamic
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the project in editable mode:**
    ```bash
    pip install -e .
    ```

### Running the Application

To start the Gradio web application, run the following command:

```bash
python app.py
```

This will start a local server, and you can access the application in your web browser at the URL provided in the console (usually `http://127.0.0.1:7860`).

### Running Tests

To run the test suite, use pytest:

```bash
pytest
```

## Project Structure

```
.
├── .github/workflows/ci.yml # GitHub Actions CI configuration
├── adamic/                   # Source code for the application
│   ├── __init__.py
│   ├── ai.py                # AI assistant logic
│   ├── bible.py             # Bible data loading and access
│   └── data/
│       └── sample_bible.json# Sample Bible data
├── app.py                   # Main application entry point (Gradio UI)
├── prd.md                   # Product Requirements Document
├── pyproject.toml           # Project metadata
├── requirements.txt         # Python dependencies
└── tests/                   # Test suite
    └── test_bible.py
```
