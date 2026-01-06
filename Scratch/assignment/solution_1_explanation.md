# Explanation: How the LLM is used for reasoning

## How the LLM is used (planning / reasoning step)

- The LLM is called only in the planning step via `generate_research_questions()`.
- The prompt asks the model to act as an expert researcher and produce a small
  list of focused research questions for the provided topic.
- This output is the LLM's "reasoning" result: instead of directly returning final
  answers, the LLM structures the problem into sub-questions that guide the agent's
  subsequent web-based information gathering (the Acting phase).

## How the reasoning step works

1. Prompting: we provide an explicit instruction to the model asking for N concise,
   well-structured questions about the topic.
2. Model output: the LLM returns text (typically numbered or bulleted). This text
   represents the LLM's decomposition of the research task — i.e., its internal
   reasoning about what aspects are important to investigate.
3. Parsing: the program splits the model output into separate lines, strips
   numbering/bullets, and stores the resulting questions for the Acting step.

This pattern follows the Planning → Acting pattern: reasoning (LLM) produces a
plan (questions) and the agent executes the plan (web searches) to gather
information.

## Code and flow explanation

- `generate_research_questions(topic, client, model, n_questions=5)`
  - Builds a concise prompt asking the LLM to produce `n_questions` research
    questions for `topic`.
  - Calls `completions_create()` (the helper) to interact with the LLM client.
  - Parses the response into a list of question strings.

- `web_search(query, max_results=3)`
  - Attempts to use `tavily` (if installed) to run a structured search and
    normalize the results.
  - If `tavily` is not available, falls back to a DuckDuckGo HTML scrape using
    `requests` + `BeautifulSoup` and returns a list of `{title, snippet}` dicts.

- `compile_report(topic, questions, search_results)`
  - Formats the gathered information into a Markdown report with sections for
    each research question and its collected snippets.

- `main()`
  - (Optional) Initializes or expects an LLM client to be wired into the
    `completions_create` helper.
  - Prompts the user for a topic and runs the pipeline:
    1. Generate questions (LLM reasoning / planning).
    2. For each question, run `web_search` (Acting) to collect web snippets.
    3. Compile the final Markdown report and save it to `output_report.md`.

## Practical notes

- The LLM performs the high-level reasoning (task decomposition). The agent
  executes the low-level actions (searching the web) and aggregates findings.
- For production use, wire a real client into the `completions_create` helper,
  ensure API keys are configured securely, and consider more robust parsing and
  source citation of web content.

---

If you want, I can also:
- Insert this explanation into the top of the generated `output_report.md`.
- Add citations / URLs into the report items collected by `web_search`.
- Wire a real Tavily/OpenAI/Gemini client and run an end-to-end test.
