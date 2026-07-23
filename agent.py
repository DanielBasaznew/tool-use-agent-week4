"""
Research Agent Engine using Gemini Native Function Calling (Week 4, Day 1)
"""

import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print

# Import tools and registry from your new tools/__init__.py
from tools import web_search, fetch_page, TOOL_REGISTRY

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

def run_agent(user_query: str, max_iterations: int = 5):
    """
    Executes a ReAct research loop using native Gemini tool calling.
    """
    print(f"\n[bold green]User Query:[/bold green] {user_query}\n")

    # System instruction guiding the model on how to research and cite sources
    system_instruction = (
        "You are an expert research assistant capable of searching the web and reading web pages. "
        "When asked a research question, follow this strategy:\n"
        "1. First, search the web using web_search with specific, targeted terms.\n"
        "2. Review the search results and select 1-2 promising URLs.\n"
        "3. Call fetch_page on those URLs to retrieve detailed facts.\n"
        "4. Synthesize the extracted facts into a coherent, comprehensive final answer with citations.\n"
        "Always provide accurate, clear, and well-cited responses."
    )

    # We pass the tools, but explicitly DISABLE automatic function calling
    # so that our loop handles the execution and prints the logs step-by-step.
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[web_search, fetch_page],
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )

    # Initialize conversation history with user prompt
    contents = [user_query]

    for iteration in range(1, max_iterations + 1):
        print(f"[bold cyan]--- Iteration {iteration} ---[/bold cyan]")

        # Protect against 5 RPM free-tier rate limits (12s per call) on multi-turn loops
        if iteration > 1:
            print("[dim gray][SYSTEM]: Pausing 2s to respect API rate limits...[/dim gray]")
            time.sleep(2)

        # Call Gemini model
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=config,
        )

        # Check if the model requested any function calls
        if response.function_calls:
            # Append model's response (with function call request) to history
            contents.append(response.candidates[0].content)

            for function_call in response.function_calls:
                fn_name = function_call.name
                fn_args = function_call.args

                print(f"[bold yellow][TOOL CALL][/bold yellow] Function: [bold]{fn_name}[/bold]")
                print(f"            Args: {fn_args}")

                # Execute the matching Python tool function
                if fn_name in TOOL_REGISTRY:
                    try:
                        tool_result = TOOL_REGISTRY[fn_name](**fn_args)
                    except Exception as e:
                        tool_result = f"Error executing tool {fn_name}: {str(e)}"
                else:
                    tool_result = f"Error: Tool '{fn_name}' is not recognized."

                print(f"[bold green][OBSERVATION][/bold green] Result length: {len(str(tool_result))} chars\n")

                # Format tool result back for Gemini's expectation
                contents.append(
                    types.Part.from_function_response(
                        name=fn_name,
                        response={"result": tool_result}
                    )
                )

        else:
            # No function calls means the model produced its final response
            final_text = response.text
            print("\n[bold magenta]=== FINAL RESPONSE ===[/bold magenta]\n")
            print(final_text)
            return final_text

    print("[bold red]Reached maximum iterations without final answer.[/bold red]")
    return None


if __name__ == "__main__":
    # Test prompt that forces web searching for up-to-date information
    test_prompt = "What is the official distance in kilometers between Paris and Tokyo?"
    run_agent(test_prompt)