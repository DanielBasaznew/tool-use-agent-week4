"""
Research Agent Engine with Structured Citation Pipeline (Week 4, Day 2)
"""

import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print

from tools import web_search, fetch_page, execute_python, read_pdf, read_pdf_page, TOOL_REGISTRY
from report_generator import generate_research_report
from display import display_report

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

def trim_messages_if_needed(contents: list, max_chars: int = 12000) -> list:
    """
    Trims the oldest messages from the conversation history if it exceeds the character limit.
    Pops items from the front (index 0) in pairs to maintain conversational flow.
    """
    while True:
        # Calculate total characters in the current conversation history
        total_chars = sum(len(str(msg)) for msg in contents)
        
        # If we are safely under the limit, or we only have 1-2 messages left, stop trimming
        if total_chars <= max_chars or len(contents) <= 2:
            break
            
        # If we are over the limit, remove the oldest memory turn (2 items)
        print(f"[bold red][SYSTEM][/bold red] Context limit approaching ({total_chars}/{max_chars} chars). Trimming oldest memory...")
        contents.pop(0)  
        if len(contents) > 0:
            contents.pop(0)
            
    return contents

def run_agent(user_query: str, max_iterations: int = 5):
    """Executes a ReAct research loop, then passes gathered facts into the Citation Engine."""
    print(f"\n[bold green]User Query:[/bold green] {user_query}\n")

    
   

    system_instruction = (
        "You are an expert research assistant capable of searching the web, reading web pages, reading PDFs, and running Python code.\n\n"
        "Strategy:\n"
        "1. Search the web using web_search with specific, targeted terms.\n"
        "2. Retrieve details from specific pages using fetch_page or local files with read_pdf.\n"
        "3. Use execute_python for calculations, data analysis, or generating charts.\n\n"
        "Grounding Rule: Base your answers and code on facts retrieved from your tools whenever available. "
        "If fetched information is missing or incomplete, search again with a refined query before concluding."
    )
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[web_search, fetch_page, execute_python, read_pdf, read_pdf_page],
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )

    contents = [user_query]
    gathered_info = ""

    for iteration in range(1, max_iterations + 1):
        print(f"[bold cyan]--- Iteration {iteration} ---[/bold cyan]")

        if iteration > 1:
            time.sleep(2)  # Protect rate limits

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=config,
        )

        if response.function_calls:
            contents.append(response.candidates[0].content)

            for function_call in response.function_calls:
                fn_name = function_call.name
                fn_args = function_call.args

                print(f"[bold yellow][TOOL CALL][/bold yellow] Function: [bold]{fn_name}[/bold]")
                print(f"            Args: {fn_args}")

                if fn_name in TOOL_REGISTRY:
                    try:
                        tool_result = TOOL_REGISTRY[fn_name](**fn_args)
                    except Exception as e:
                        tool_result = f"Error executing tool {fn_name}: {str(e)}"
                else:
                    tool_result = f"Error: Tool '{fn_name}' is not recognized."

                print(f"[bold green][OBSERVATION][/bold green] Result length: {len(str(tool_result))} chars\n")

                # Accumulate raw observations into our research bank for citation generation
                gathered_info += f"\n--- Source Data ({fn_name}) ---\nArgs: {fn_args}\nResult:\n{tool_result}\n"

                contents.append(
                    types.Part.from_function_response(
                        name=fn_name,
                        response={"result": tool_result}
                    )
                )

        else:
            # ReAct phase complete! Pass raw gathered info to structured citation pipeline
            print("\n[bold yellow]Generating Structured Citation Report...[/bold yellow]\n")
            
            # If model answered directly without tool output, use its response text
            if not gathered_info.strip():
                gathered_info = response.text

            report = generate_research_report(user_query, gathered_info)
            display_report(report)
            return report

    print("[bold red]Reached maximum iterations without completing research.[/bold red]")
    return None


if __name__ == "__main__":
    print("=== Welcome to the ReAct Research Agent ===")
    user_input = input("Enter your research request: ").strip()
    
    if user_input:
        run_agent(user_input)
    else:
        print("No input provided. Exiting.")