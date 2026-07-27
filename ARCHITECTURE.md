# System Architecture: ReAct Research Agent

This document outlines the internal architecture and data flow of the Autonomous Research Agent. 

## 1. The ReAct Loop (Reasoning + Acting)
At the core of the agent is a `while` loop that implements the ReAct paradigm. Instead of just generating a text response, the LLM is prompted to "think" about what it needs to do, and then "act" by selecting a tool.

1. **User Input:** The query is appended to the message history.
2. **Generation:** The model processes the history and generates a response.
3. **Evaluation:**
   * If the model outputs a `function_call` (an action), the system intercepts it.
   * If the model outputs raw text, the loop terminates, and the response is parsed.
4. **Execution:** The selected tool is executed locally, and the observation (result) is appended back into the message history as a `function_response`.
5. **Iteration:** The loop restarts, allowing the model to reason about the new data.

## 2. Dynamic Context Window Management
LLMs have strict token limits. During deep research, fetching web pages and reading PDFs quickly floods the context window, leading to API crashes.

To solve this, the agent uses a **Message Pruning Pipeline** (`trim_messages_if_needed`).
* **Threshold Detection:** After every tool observation, the script counts the total characters in the `message_history`.
* **Safe Eviction:** If the limit is exceeded, the function pops the oldest historical messages (excluding the system prompt and the current query) until the context is safe.
* **Preservation:** This ensures the agent "forgets" outdated search results but retains the overarching goal and the most recent findings.

## 3. Tool Registry & Sandboxing
The agent is equipped with a specific toolset, structured via Pydantic schemas or standard Python type hints to ensure the LLM knows exactly how to invoke them:

* **`web_search`:** Uses DuckDuckGo to fetch non-API-restricted search snippets.
* **`fetch_page`:** Uses `requests` and `BeautifulSoup4`. It specifically cleans out navigation, scripts, and footers to maximize token efficiency, and truncates text to prevent overflow.
* **`read_pdf` / `read_pdf_page`:** Uses `pypdf` to extract text from local files.
* **`execute_python`:** 
  * Runs dynamically generated AI code using `subprocess.run()`.
  * **Security & Stability:** Implements a strict 15-second `timeout` to prevent infinite loops and captures both `stdout` and `stderr` so the model can read stack traces if its code crashes.

## 4. Grounding & Citation (Structured Output)
To prevent hallucination ("citation theater"), the agent is governed by strict system prompts forcing it to use extracted data rather than its training memory. 

Upon completing the research loop, a separate structured output call is made (using Instructor/Pydantic or Gemini's structured outputs) to format the final answer into a clean, rich-text Citation Report containing a summary, key findings, and a sources table.