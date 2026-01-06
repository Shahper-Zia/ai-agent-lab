# LangChain Assignment — Intelligent Travel Assistant

## Problem Statement

Build an intelligent Travel Assistant AI that, given a user-provided destination, returns:

- The current weather forecast for the destination (via a custom weather tool).
- Top local attractions and points of interest (via a search tool).

## Goals

- Implement a LangChain agent that calls multiple tools.
- Provide a good user experience: user supplies a destination, agent returns weather + attractions.

## Approach

1. LangChain Agent
	- Use a tool-calling agent to orchestrate calls to the weather tool and a web-search tool.

2. Custom Tools
	- Weather tool: Implement using LangChain's `@tool` decorator to fetch current weather (e.g., WeatherAPI.com).
	- Search tool: Use an available search agent (DuckDuckGo, Tavily, or similar) to find top attractions.

3. Agent Creation
	- Use LangChain's tool-calling utilities (for example, `create_tool_calling_agent`) to bind tools and create an agent.
	- Use `AgentExecutor` (or the equivalent orchestration API) to run the agent.

4. User Interaction
	- The program accepts a destination (city or location) and returns:
	  - A concise weather summary.
	  - A list of recommended attractions with short descriptions.

## Architecture & Steps to Implement

1. Install dependencies

```bash
pip install langchain requests
```

2. Configure an LLM

- Choose an LLM for summarization and reasoning (OpenAI, Google Gemini, or another supported model). Configure credentials as required by the provider.

3. Weather API setup

- Sign up for an API key (e.g., WeatherAPI.com) and store the key in an environment variable (e.g., `WEATHER_API_KEY`).

4. Search agent setup

- Configure and authorize a web-search tool (DuckDuckGo/Tavily or another supported search connector).

5. Implement the Weather tool

- Create a function that calls the weather API and returns a short forecast string. Wrap it with LangChain's `@tool` decorator so the agent can call it.

6. Implement the Search tool

- Use a search connector or write a small scraper/search wrapper to return the top attractions and brief descriptions.

7. Create the tool-calling agent

- Register both tools with the agent and build an agent capable of calling them and composing the final answer.

8. Run and test

- Provide a sample input (e.g., `Paris`) and verify the agent returns weather + attractions.

## Example Usage (conceptual)

1. User inputs: "Tokyo"
2. Agent calls: `weather_tool("Tokyo")` -> returns forecast.
3. Agent calls: `search_tool("top attractions in Tokyo")` -> returns attractions list.
4. Agent composes and returns a concise response.

## Expected Deliverables

1. Code
	- A Python script or Jupyter notebook implementing the Travel Assistant using an LLM, a web search tool, and a weather tool.

2. Report (Markdown)
	- A short explanation describing how the LLM is used for reasoning and summarization.
	- An explanation of the code structure and program flow.

## Notes & Tips

- Use environment variables for API keys and model credentials.
- Keep tool outputs concise to make LLM summarization easier.
- Include error handling for network/API failures and unknown destinations.

---

If you want, I can also:

- Provide a starter Python script that implements the weather tool and a simple search wrapper.
- Create a sample Jupyter notebook demonstrating the agent flow.
