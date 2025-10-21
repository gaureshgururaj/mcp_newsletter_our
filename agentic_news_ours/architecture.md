# Agentic News System Architecture

This document breaks down the architecture and workflow of the Agentic News Summarization system.

## System Architecture and Workflow

This diagram shows the two main parts of the system: the **User Interface** and the **Agentic Backend**. The workflow proceeds sequentially from the user's input, through each specialized agent, until the final report is generated and displayed.

```mermaid
graph TD
    subgraph "User Interface (Streamlit)"
        UI_Input["User Enters Topic & Time Period"]
        UI_Button["Clicks 'Generate Summary'"]
        UI_Display["Displays Final Report"]
    end

    subgraph "Agentic Backend (CrewAI)"
        A["<b>1. Research Agent</b><br/>Finds relevant articles using the Tavily API.<br/><i>Tool: TavilySearchTool</i>"]
        B["<b>2. Validation Agent</b><br/>Checks each source for factual accuracy and reliability.<br/><i>Tool: ValidationTools</i>"]
        C["<b>3. Analysis Agent</b><br/>Synthesizes validated findings to identify key themes.<br/><i>Tool: AnalysisTools</i>"]
        D["<b>4. Content Generation Agent</b><br/>Writes the first draft of the news article.<br/><i>Tool: WriteFileTool</i>"]
        E["<b>5. Senior Editor Agent</b><br/>Reviews, edits, and formats the final report.<br/><i>Tools: ReadFileTool, EditingTools, WriteFileTool</i>"]
    end

    subgraph "Configuration Files"
        AgentsYAML["fa:fa-file-code agents.yaml<br/>(Defines agent personas, goals, backstories)"]
        TasksYAML["fa:fa-file-code tasks.yaml<br/>(Defines task descriptions and expected outputs)"]
    end

    subgraph "Data & External APIs"
        TavilyAPI["fa:fa-server Tavily Search API"]
        InitialReport["fa:fa-file-alt initial_report.md"]
        FinalReport["fa:fa-file-alt final_report.md"]
    end

    %% --- Workflow Connections ---
    UI_Input --> UI_Button
    UI_Button -- "Kicks off the Crew" --> A

    A -- "Uses" --> TavilyAPI
    A -->|"List of Findings"| B
    
    B -->|"Validated Findings"| C

    C -->|"Structured Analysis"| D
    
    D -- "Writes to" --> InitialReport
    D -->|"Draft Content"| E
    
    E -- "Reads from" --> InitialReport
    E -- "Writes to" --> FinalReport
    
    FinalReport -->|"Sends to"| UI_Display

    %% --- Configuration Connections ---
    A & B & C & D & E -- "Configured by" --> AgentsYAML
    A & B & C & D & E -- "Configured by" --> TasksYAML

```

## How to Explain This to Your Team

1.  **Start with the User:** The process begins in the Streamlit UI, where a user enters a topic.
2.  **The Crew Kicks Off:** This triggers our `NewsSummarizationCrew`. The crew is configured using two YAML files: `agents.yaml` for defining *who the agents are* (their personalities and goals) and `tasks.yaml` for *what they do* (their specific instructions).
3.  **The Research Agent:** The first agent takes the topic and uses the **Tavily API** to find recent, relevant articles. It passes a list of its findings to the next agent.
4.  **The Validation Agent:** This agent acts as a fact-checker. It reviews the sources from the researcher and assigns a confidence score, filtering out unreliable information.
5.  **The Analysis Agent:** This agent looks for the "so what." It takes the validated facts and synthesizes them, identifying the key themes and narratives.
6.  **The Content Generation Agent:** Using the analysis, this agent writes the first draft of the news report and saves it as `initial_report.md`.
7.  **The Senior Editor Agent:** The final agent reads the draft, edits it for style, grammar, and clarity, and then writes the polished `final_report.md`.
8.  **Display the Report:** The system serves this final markdown file back to the Streamlit UI for the user to read.

This entire process ensures a "chain of evidence," where the final report is built upon layers of validated and analyzed information, reducing the risk of errors and hallucinations. 