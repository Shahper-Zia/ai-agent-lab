# Travel Assistant — Report

## i. How the LLM is used for reasoning

- Role: The LLM acts as the controller and composer. It receives the user query, classifies the query type, decides which tools to call, and synthesizes tool outputs into a concise Markdown response.
- Decision logic (high-level):
  1. Validate and classify the query (Specific destination vs. Exploratory/thematic).
  2. For Specific queries: call both `get_weather` and `get_top_attractions` tools to fetch factual data.
  3. For Exploratory/thematic queries: call `get_top_attractions` as needed; call `get_weather` only when a specific destination is selected or the user requests real-time weather.
  4. Compose a final, user-facing Markdown answer that clearly separates tool-provided facts from general travel guidance.
- Reasoning step (safe summary): the LLM uses a structured prompt (the system prompt) that encodes flows, tool-usage rules, and response formatting. The model follows that policy to choose tools and combine outputs. This is a procedural/algorithmic use of the LLM — not an unconstrained chain-of-thought — and results in deterministic, tool-grounded outputs when the prompt and tools are fixed.

## ii. Code and program flow (overview)

High-level components and flow:

1. Environment & helpers
   - A `requests` session is configured with a browser-like `User-Agent` header to improve scraping reliability.
   - A `MarkItDown` and `BeautifulSoup` helper is used to extract title and textual content from web pages.
   - `TavilySearch` (or another search connector) is configured as `tavily_tool` to return search results.

2. Tools (LangChain `@tool` functions)
   - `get_top_attractions(destination: str) -> list`:
     - Builds a search prompt for top attractions in the destination.
     - Invokes `tavily_tool.invoke(...)` to get search results.
     - Concurrently extracts page contents (title + text) using `MarkItDown` and a `ThreadPoolExecutor` with timeouts and fallbacks.
     - Returns a list of concise documents (each containing title + extracted text) for the agent to consume.

   - `get_weather(query: str) -> dict`:
     - Calls WeatherAPI (configured via `WEATHER_API_KEY` environment variable) using its `current.json` endpoint.
     - Returns parsed JSON weather data or a clear "Weather Data Not Found" message when unavailable.

3. System prompt (agent rules)
   - A detailed `AGENT_PREFIX` / `SYS_PROMPT` defines the agent’s role, capabilities, and the two query flows (A: Specific Destination, B: Exploratory/Thematic).
   - The prompt enforces rules: which tools must/may be used, when to call `get_weather`, and how to format responses (Markdown, separate factual vs. general guidance).

4. Agent creation
   - An LLM instance (the notebook uses a configured LLM) is passed to `create_agent(...)` along with the `tools` list and the `SYS_PROMPT`.
   - The agent implements a ReAct-like loop: interpret the user input, decide on tool calls, call tools, and produce final output.

5. Running and streaming
   - The notebook demonstrates streaming calls to the agent (with `travel_assistant.stream(...)`) so intermediate events can be observed during execution.
   - A helper `call_travel_assistant_agent(query, verbose=False)` wraps the streaming call and displays the final agent-generated Markdown output.

6. Example interactions
   - Example queries shown in the notebook:
     - "I am planning a trip to Tokyo. Suggest place based on weather and attractions." (Specific destination — both tools used.)
     - "In India where I should visit during summer?" (Exploratory — may use only attraction tool.)
     - "In India I am planning to visit south, when i should go suggest me best time to enjoy its peak beauty." (Exploratory/thematic — agent classifies intent and responds according to Flow B.)

## Implementation notes & recommendations

- Credentials: store `WEATHER_API_KEY` and any search-provider credentials in environment variables.
- Timeouts and fallbacks: the `get_top_attractions` tool uses timeouts and fallback content extraction to maintain robustness.
- Output formatting: keep tool outputs concise so the LLM can summarize them effectively.
- Error handling: present clear, actionable messages when a tool fails (e.g., weather data not found).

---