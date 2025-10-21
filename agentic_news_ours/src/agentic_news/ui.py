import streamlit as st
import os
from agentic_news.crew import NewsSummarizationCrew

def run_crew(topic: str, time_period: str):
    """
    Runs the News Summarization Crew with a given topic and time period.
    The crew will write its final report to 'final_report.md'.
    """
    # Map the UI selection to the values Tavily expects
    time_range_map = {
        "Any time": None,
        "Last 24 hours": "d",
        "Last week": "w",
        "Last month": "m",
        "Last year": "y",
    }
    selected_time_range = time_range_map[time_period]

    inputs = {"topic": topic, "time_period": selected_time_range}
    crew = NewsSummarizationCrew().crew()
    crew.kickoff(inputs=inputs)

# --- Page Configuration ---
st.set_page_config(
    page_title="Agentic News",
    page_icon="📰",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("📰 Controls")
st.sidebar.info(
    "Enter a topic and select a time period to start the news summarization process."
)

topic = st.sidebar.text_input(
    "News Topic",
    placeholder="e.g., The latest on self-driving cars",
    key="topic_input",
)

time_period = st.sidebar.selectbox(
    "Time Period",
    ("Any time", "Last 24 hours", "Last week", "Last month", "Last year"),
    index=1,
)

st.sidebar.selectbox(
    "Content Type",
    ("Text", "Voice", "Video"),
    key="content_type_input",
    help="Select the type of content to generate (Placeholder).",
)

st.sidebar.selectbox(
    "Language",
    (
        "English",
        "Mandarin Chinese",
        "Hindi",
        "Spanish",
        "French",
        "German",
        "Russian",
        "Arabic",
        "Italian",
        "Korean",
        "Punjabi",
        "Bengali",
        "Portuguese",
        "Indonesian",
        "Urdu",
        "Persian (Farsi)",
        "Vietnamese",
        "Polish",
        "Samoan",
        "Thai",
        "Ukrainian",
        "Turkish",
        "Norwegian",
        "Dutch",
        "Greek",
        "Romanian",
        "Swahili",
        "Hungarian",
        "Hebrew",
        "Swedish",
        "Czech",
        "Finnish",
        "Tagalog",
        "Burmese",
        "Tamil",
        "Kannada",
        "Pashto",
        "Yoruba",
        "Malay",
        "Haitian Creole",
        "Nepali",
        "Sinhala",
        "Catalan",
        "Malagasy",
        "Latvian",
        "Lithuanian",
        "Estonian",
        "Somali",
        "Maltese",
        "Corsican",
        "Luxembourgish",
        "Occitan",
        "Welsh",
        "Albanian",
        "Macedonian",
        "Icelandic",
        "Slovenian",
        "Galician",
        "Basque",
        "Azerbaijani",
        "Uzbek",
        "Kazakh",
        "Mongolian",
        "Lao",
        "Telugu",
        "Marathi",
        "Chichewa",
        "Esperanto",
        "Tajik",
        "Yiddish",
        "Zulu",
        "Sundanese",
        "Tatar",
        "Tswana",
    ),
    key="language_input",
    help="Select the language for the report (Placeholder).",
)

if st.sidebar.button("Generate Summary"):
    # --- Main Content ---
    st.title(f"🗞️ Agentic News Report: {topic}")
    st.markdown("---")
    if topic:
        with st.spinner("🤖 Agents are at work... This may take a few minutes..."):
            try:
                run_crew(topic, time_period)

                if os.path.exists("final_report.md"):
                    with open("final_report.md", "r", encoding="utf-8") as file:
                        report_content = file.read()
                    st.markdown(report_content)
                else:
                    st.error(
                        "The final report was not generated. Please check the console for errors."
                    )
            except Exception as e:
                st.error(f"An error occurred while running the agentic system: {e}")
    else:
        st.warning("Please enter a topic in the sidebar to generate a summary.")
else:
    st.info("Enter a topic in the sidebar and click 'Generate Summary' to begin.")

# --- Footer ---
st.markdown("---")
st.markdown("*Powered by CrewAI Framework*") 