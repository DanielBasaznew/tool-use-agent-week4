# Day 1 Journal: Research Agent Foundation & Native Schemas

### Technical Reflection: Search Snippets vs. Fetched Pages
A 200-character search snippet acts as a lightweight index—it is fast, cheap, and allows the agent to scan multiple sources without clogging the context window. Snippets are ideal for direct factual queries (like calculating distances or checking simple dates). A 2,000-character fetched page provides deep context necessary for comprehensive analysis, code summaries, or multi-step synthesis. However, full pages consume significantly more context window capacity and add network latency. A production agent should use snippets to evaluate source relevance and reserve full-page fetching only when deep context is strictly required.

### Daily Experience & Key Engineering Takeaway
Today was a challenging build day due to unexpected API rate limits (429 errors) and model deprecation issues. Transitioning to `gemini-3.1-flash-lite`, disabling automatic function calling to observe the intermediate ReAct loop, and adding explicit execution pauses (`time.sleep`) resolved the quota bottlenecks. Migrating from manual string parsing to formal JSON schemas is a major upgrade—it creates predictable, structured tool invocations that mirror how production AI agents are built in the real world.

# Day 2: Citation Engine & Structured Outputs

### Technical Reflection
Requiring an AI agent to cite its sources fundamental transforms its role from a probabilistic text generator into a grounded research tool. By enforcing a structured Pydantic schema (`ResearchReport` with `Source` items), the model is forced to map every assertion directly back to specific titles and key points retrieved during the ReAct phase. 

This strict schema-bound mapping drastically reduces hallucinations—the LLM cannot fabricate claims without failing its contract to trace them back to extracted context. Structured outputs convert raw web clutter into predictable, audit-ready data suitable for downstream applications.

# Day 3: Python Code Execution Tool & Subprocess Safety

### Technical Reflection
Giving an LLM code execution capabilities elevates its reasoning from textual approximation to deterministic computation. Instead of estimating math or algorithms, the agent writes executable Python code, runs it in an isolated process, and incorporates the `stdout` results into its reasoning loop.

### Security & Architecture
Executing unverified model-generated code introduces significant security risks:
- **Naive Evaluation Risk:** Never use Python's native `eval()` or `exec()` in production, as they execute within the main application process with full access to host memory, environment variables, and system resources.
- **Subprocess Isolation:** Our `execute_python` tool uses `subprocess.run` with a strict 15-second timeout to prevent infinite loops, and enforces a dedicated temporary working directory (`tempfile.gettempdir()`) to isolate file outputs (like charts or plots) from project source code.
- **Production Sandboxing:** While local subprocesses protect basic file structures, enterprise production systems (like OpenAI Code Interpreter, E2B, or Modal) use hardened MicroVMs/Docker containers with strict network isolation, memory caps, and non-root execution environments to guarantee multi-tenant safety.

# Day 4: PDF Extraction & Interactive Document Q&A

### Technical Reflection
Parsing PDF documents requires distinguishing between digital text extraction and Optical Character Recognition (OCR). Digital PDFs store vector characters that PyMuPDF (`fitz`) can extract directly. In contrast, scanned PDFs contain only pixel images; extracting text from them requires an OCR engine (such as Tesseract or PaddleOCR).

To optimize context window usage, we implemented a two-tier extraction pattern:
1. `read_pdf`: Provides an initial document summary and first-chunk overview capped at 3,000 characters.
2. `read_pdf_page`: Fetches full text for specific 1-indexed pages on demand.

When tested against a scanned image PDF (`photo-print.pdf`), the tool failed safely by returning a warning that no extractable text characters were found, preventing context pollution or model hallucination.

# Day 5: Unified Multi-Tool Research Agent & Context Window Protection

### Technical Reflection
Combining multiple tools (web search, web fetching, Python execution, and PDF reading) into a single ReAct loop reveals key insights into model orchestration and context window limits:

1. **Context Window Protection:** Multi-step agent loops accumulate large amounts of raw text from webpage fetches and PDF overviews. Implementing `trim_messages_if_needed` protects the system from context overflow errors by popping the oldest non-system conversation turns when character counts exceed threshold limits.
2. **Tool Selection Behavior & Path of Least Resistance:** When presented with 5 tools, the agent frequently optimizes for the simplest path to fulfill prompt requirements. For instance, rather than downloading and parsing online PDFs or writing complex web-scraping scripts, it leverages web search snippets and injects gathered facts directly into executable Python scripts.
3. **Grounding vs. Helpfulness Conflict:** Even with strict system prompts forbidding the use of training memory, the agent will sometimes break the rules if the fetched data is truncated (e.g., Wikipedia tables being cut off). The model prioritizes generating a helpful output (like rendering the requested chart) over strict adherence to data provenance rules, highlighting the need for more robust data extraction pipelines in future iterations.