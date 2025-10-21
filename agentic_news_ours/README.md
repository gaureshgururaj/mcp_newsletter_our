# Agentic News Summarization System

This project is a sophisticated, multi-agent system designed to research, analyze, and summarize news on any given topic. It leverages the CrewAI framework to orchestrate a team of specialized AI agents, each with a distinct role, ensuring a comprehensive and factual final report.

The system is designed to combat AI hallucinations by implementing a strict chain of evidence, where every claim in the final output is traceable to a validated source.

## Features

- **Multi-Agent Collaboration**: Utilizes a crew of agents (Research, Validation, Analysis, Content Generation, and Editing) to divide and conquer the task.
- **Dynamic Topic Analysis**: Can research and generate reports on any user-provided topic.
- **Fact-Checked and Validated**: Includes a dedicated validation agent to check sources and score information for reliability.
- **Clickable Sources**: The final report includes a "Sources" section with clickable markdown links to all original articles.
- **Time-Bound Searches**: Filter news results by time period (e.g., "Last 24 hours," "Last week") directly from the UI for more relevant results.
- **Interactive UI**: A user-friendly interface built with Streamlit, featuring sidebar controls for a clean layout.
- **Extensible Framework**: Easily customizable by modifying agent roles and task descriptions in YAML configuration files.

## Project Structure

The project is organized to separate configuration, tools, and the main application logic, making it easy to maintain and extend.

```
agentic_news/
├── .venv/                      # Virtual environment
├── architecture.md             # System architecture and workflow diagram
├── knowledge/
│   └── user_preference.txt
├── src/
│   └── agentic_news/
│       ├── __init__.py
│       ├── config/
│       │   ├── agents.yaml     # Definitions of agent roles, goals, and backstories
│       │   └── tasks.yaml      # Descriptions and expected outputs for each task
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── custom_tool.py  # Custom tools for reading/writing files, editing, etc.
│       │   └── search_tools.py # Custom tool for web searches using Tavily
│       ├── crew.py             # Main crew definition, agent and task instantiation
│       ├── main.py             # Command-line entry point to run the crew
│       └── ui.py               # Streamlit user interface
├── final_report.md             # Default output file for the final report
├── pyproject.toml
├── README.md                   # This file
└── requirements.txt            # Project dependencies
└── uv.lock
```

## Setup and Installation

This project uses `uv` for package and environment management. For a basic `crewai` installation guide, you can refer to this [document](https://docs.google.com/document/d/1R3_L_JvNhn0GSUkC7oJKOgShoyU6iaNVAVUsPMmkeI8/edit?tab=t.0).

### 1. Create and Activate Virtual Environment

First, create a virtual environment using `uv`:

```bash
uv venv
```

Activate the virtual environment.

On Windows:
```powershell
.venv\Scripts\activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

Install all the required Python packages from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### 3. Set Up Environment Variables

The application requires API keys for OpenAI and Tavily Search.

Create a `.env` file in the project's root directory by copying the example below:

```.env
# .env.example

# --- LLM Provider ---
# Choose your preferred LLM provider and model.
# Example for OpenAI:
OPENAI_API_KEY="sk-..."
# Example for Groq:
# GROQ_API_KEY="gsk_..."

# --- Search Tool ---
# Tavily is used for web searches.
TAVILY_API_KEY="tvly-..."
```

Replace the placeholder values with your actual API keys.

## Usage

You can run the agentic system in two ways:

### 1. Interactive Streamlit UI (Recommended)

To launch the web-based user interface, run the following command from the project root:

```bash
uv run python -m streamlit run src/agentic_news/ui.py
```

Navigate to `http://localhost:8501` in your web browser. Enter a topic and click "Generate Summary" to start the crew.

### 2. Command-Line Interface

To run the crew directly from the command line for a specific topic:

```bash
uv run python -m src.agentic_news.main "Your Topic Here"
```

For example:
```bash
uv run python -m src.agentic_news.main "The future of quantum computing"
```

The final report will be saved to `final_report.md` in the project root.

## How It Works: The Agents and Their Tasks

The system is composed of five agents that execute tasks sequentially:

1.  **Research Agent**: Receives the topic and uses the Tavily search tool to find relevant articles and sources.
2.  **Validation Agent**: Scrutinizes each source from the research agent. It checks for factual accuracy and assigns a confidence score to each piece of information.
3.  **Analysis Agent**: Synthesizes the validated information, identifies key themes and sentiment, and creates a structured analysis report.
4.  **Content Generation Agent**: Uses the analysis report to write a full, well-structured news article.
5.  **Senior Editor Agent**: Performs the final review, checking for grammatical errors, stylistic consistency, and factual accuracy. It then formats the final report, ensuring the "Sources" section contains clickable links.

This structured process ensures that the final output is not only well-written but also thoroughly vetted and factually grounded.

For a detailed visual representation of the agent workflow and system architecture, please see the [Architecture Diagram](architecture.md).

## Support

For support, questions, or feedback regarding the AgenticNews Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
