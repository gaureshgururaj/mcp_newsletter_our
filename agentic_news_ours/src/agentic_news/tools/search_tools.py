import os
from typing import Optional, Type
from crewai.tools import BaseTool
from tavily import TavilyClient
from pydantic import BaseModel, Field


class TavilySearchToolSchema(BaseModel):
    """Input for TavilySearchTool."""

    query: str = Field(..., description="The search query to be used.")
    time_period: Optional[str] = Field(
        description="The time period to filter the search results. e.g., 'd', 'w', 'm', 'y'."
    )


class TavilySearchTool(BaseTool):
    name: str = "Tavily Search"
    description: str = "A tool that uses the Tavily API to search the web for information."
    args_schema: Type[BaseModel] = TavilySearchToolSchema

    def _run(
        self, query: str, time_period: Optional[str] = None
    ) -> str:
        """
        Performs a search using the Tavily client and returns the results.
        An optional time_period can be provided to filter results.
        """
        try:
            api_key = os.environ.get("TAVILY_API_KEY")
            if not api_key:
                raise ValueError("Tavily API key not found in environment variables.")

            client = TavilyClient(api_key=api_key)

            search_kwargs = {
                "query": query,
                "search_depth": "basic",
                "topic": "news",  # Required for time-based filtering
            }
            if time_period:
                search_kwargs["time_range"] = time_period

            response = client.search(**search_kwargs)
            return response["results"]
        except Exception as e:
            # Instead of returning a string, we re-raise the exception
            # so the agent can see the full error details.
            raise e 