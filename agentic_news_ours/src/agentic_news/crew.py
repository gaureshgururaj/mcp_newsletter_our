from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool

load_dotenv()

from .tools.search_tools import TavilySearchTool
from .tools.custom_tool import (
    ValidationTools,
    AnalysisTools,
    
    EditingTools,
    WriteFileTool,
    ReadFileTool,
)

scrape_tool = ScrapeWebsiteTool()

@CrewBase
class NewsSummarizationCrew:
    """NewsSummarizationCrew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            tools=[TavilySearchTool()],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["validation_agent"],
            tools=[ValidationTools()],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["analysis_agent"],
            tools=[AnalysisTools()],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def content_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["content_generation_agent"],
            tools=[WriteFileTool()],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def senior_editor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_editor_agent"],
            tools=[EditingTools(), ReadFileTool(), WriteFileTool()],
            llm=self.llm,
            verbose=True,
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.research_agent(),
        )

    @task
    def validation_task(self) -> Task:
        return Task(
            config=self.tasks_config["validation_task"],
            agent=self.validation_agent(),
            context=[self.research_task()],
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],
            agent=self.analysis_agent(),
            context=[self.validation_task()],
        )

    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_generation_task"],
            agent=self.content_generation_agent(),
            output_file="initial_report.md",
            context=[self.analysis_task()],
        )

    @task
    def senior_editor_task(self) -> Task:
        return Task(
            config=self.tasks_config["senior_editor_task"],
            agent=self.senior_editor_agent(),
            output_file="final_report.md",
            context=[self.content_generation_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the news summarization crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
