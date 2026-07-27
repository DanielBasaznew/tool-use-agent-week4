# 🤖 ReAct Autonomous Research Agent

An autonomous research agent built in Python that implements the **ReAct (Reasoning + Acting)** framework. The agent autonomously decides when to search the web, fetch and parse web content, read local PDF documents, and execute sandboxed Python code to analyze data or generate visualizations.

---

## 🌟 Key Features

- 🌐 **Web Search & Scraping** – Performs web searches and extracts clean, structured body text and HTML tables using **BeautifulSoup4**.
- 🐍 **Sandboxed Python Execution** – Executes dynamically generated Python code in an isolated subprocess with timeout protection. Supports **Pandas** for data analysis and **Matplotlib** for visualization.
- 📄 **PDF Document Q&A** – Reads complete PDF documents or specific pages to extract research methodology, key findings, and other information.
- 🛡️ **Context Window Protection** – Automatically trims old conversation history using the `trim_messages_if_needed()` pipeline to prevent context overflow during long reasoning sessions.
- 📊 **Rich Terminal Output** – Displays formatted reports, highlighted findings, and structured citation tables using the **Rich** library.

---

## 🏗️ Architecture Overview

The agent follows an iterative **ReAct** workflow:

```text
              ┌──────────────────────────────┐
              │          User Query          │
              └──────────────┬───────────────┘
                             │
                             ▼
               ┌───────────────────────────┐
               │    LLM Reasoning Step     │
               └─────────────┬─────────────┘
                             │
                    [Decides Tool Call]
                             │
                             ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
     │ web_search   │  │ fetch_page   │  │ execute_python   │ 
     └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
            │                 │                   │
            └─────────────────┼───────────────────┘
                              │
                              ▼
                  [Observation Returned]
                              │
                              ▼
              ┌────────────────────────────┐
              │ Prune Memory Context       │
              │ trim_messages_if_needed()  │
              └──────────────┬─────────────┘
                             │
                     (Repeat Until Done)
                             │
                             ▼
              ┌────────────────────────────┐
              │ Structured Final Report    │
              └────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.10+ |
| **AI Model & SDK** | Google Gemini API (`google-genai`) |
| **Web Scraping** | `requests`, `BeautifulSoup4` |
| **Data Processing** | `pandas` |
| **Visualization** | `matplotlib` |
| **PDF Parsing** | `pypdf` |
| **Terminal UI** | `rich` |

---

# 🚀 Quickstart Guide

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/tool-use-agent-week4.git
cd tool-use-agent-week4
```

---

## 2. Create and Activate a Virtual Environment

### Windows (PowerShell / Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install google-genai beautifulsoup4 matplotlib pandas pypdf rich pydantic python-dotenv
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project's root directory.

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 5. Run the Agent

```bash
python agent.py
```

---

# 💡 Example Prompts

### 🌐 Web Research & Data Visualization

> Search for the current GDP of the top 5 economies in the world, then generate a bar chart and save it as `gdp_chart.png`.

---

### 🐍 Python Data Analysis

> Create a Pandas DataFrame showing global renewable energy adoption trends over the last five years, generate a plot, and save it as an image.

---

### 📄 Local PDF Question Answering

> Read the PDF at `path/to/document.pdf` and summarize its methodology and conclusions.

---

### 🤖 Multi-Tool Autonomous Workflow

> Search for a recent academic paper about AI agents, fetch the article, extract the methodology, visualize any reported data using Python, and produce a cited summary.

---

## 🛡️ Safety & Limitations

- **Execution Timeout** – Python scripts execute inside an isolated subprocess with a **15-second timeout** to prevent infinite loops.
- **Scanned PDFs** – OCR is **not** included. Image-only PDFs must be processed with an OCR tool before use.
- **Context Protection** – Web page content is automatically truncated when necessary to stay within the model's context window while preserving important tables and information.

## 📂 Project Structure

```text
tool-use-agent-week4/
│
├── agent.py                  # Main ReAct autonomous agent
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables (ignored by Git)
├── README.md                 # Project documentation
│
├── tools/
│   ├── web_search.py         # Web search tool
│   ├── fetch_page.py         # Web page scraper
│   ├── execute_python.py     # Sandboxed Python execution
│   ├── pdf_reader.py         # PDF parsing utilities
|   ├── __init__.py           # For tool registery       
│   └── ...                   # Additional tools
│
├── outputs/                  # Generated charts and files
│
└── .venv/                    # Python virtual environment (optional)
```

---

## 🧠 How It Works

The agent follows the **ReAct (Reasoning + Acting)** paradigm.

1. The user submits a research question.
2. The LLM reasons about what information is needed.
3. The model decides whether a tool should be called.
4. The selected tool executes and returns an observation.
5. The observation is added to the conversation history.
6. Old context is trimmed automatically when necessary.
7. The loop repeats until the model has enough information.
8. The agent produces a final structured response with citations and generated artifacts.

This iterative reasoning loop enables the agent to solve complex multi-step tasks that require combining information from multiple sources.

---

## 🔧 Available Tools

| Tool | Purpose |
|------|---------|
| **web_search** | Searches the web for relevant information. |
| **fetch_page** | Downloads and extracts readable text from web pages. |
| **execute_python** | Runs Python code in an isolated subprocess for analysis and visualization. |
| **read_pdf** | Extracts an overview from an entire PDF document. |
| **read_pdf_page** | Reads the full text of a specific PDF page on demand. |

---

## 📸 Example Output

Example research workflow:

```text
User:
Search for the five largest economies by GDP,
create a bar chart,
and summarize your findings.

↓

Reasoning...

↓

Searching the web...

↓

Fetching source pages...

↓

Generating Python code...

↓

Executing Python...

↓

Chart saved:
outputs/gdp_chart.png

↓

Final Answer:
• GDP rankings
• Bar chart generated
• Sources cited
```

---

## ⚙️ Configuration

The project can be customized by modifying parameters inside the source code.

Some configurable settings include:

- LLM model name
- Temperature
- Maximum context size
- Python execution timeout
- Web page extraction length
- PDF overview length
- Output directory

These values can be adjusted depending on the desired balance between speed, cost, and reasoning quality.

---

## 🚀 Future Improvements

Planned enhancements include:

- ✅ OCR support for scanned PDFs
- ✅ Persistent long-term memory using vector databases
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Multi-document reasoning
- ✅ Image understanding
- ✅ Streaming responses
- ✅ Parallel tool execution
- ✅ Docker support
- ✅ Unit and integration testing
- ✅ Web interface (FastAPI or Streamlit)

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve this project:

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature/my-feature
```

3. Commit your changes.

```bash
git commit -m "Add my new feature"
```

4. Push your branch.

```bash
git push origin feature/my-feature
```

5. Open a Pull Request.

Please follow the existing coding style and include documentation for any new functionality.

---

## 📚 References

- ReAct: *Reasoning and Acting in Language Models* (Yao et al., 2022)
- Google Gemini API Documentation
- BeautifulSoup4 Documentation
- Pandas Documentation
- Matplotlib Documentation
- Rich Documentation
- PyPDF Documentation

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## 👨‍💻 Author

**Daniel Basaznew**

• ML Engineer  • Python Developer • AI & Automation Enthusiast

Passionate about building intelligent systems that combine reasoning, tool use, automation, and data analysis.

---

## ⭐ Support

If you found this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest new features
- 🤝 Contribute improvements

Your support helps make the project better for everyone.