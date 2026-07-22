import os
import fitz  # PyMuPDF
import pandas as pd
import requests
from dotenv import load_dotenv
from rich import print

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("[bold green]✓ Imports successful![/bold green]")
print(f"PyMuPDF version: [cyan]{fitz.__version__}[/cyan]")
print(f"Pandas version: [cyan]{pd.__version__}[/cyan]")

if api_key and api_key != "your_actual_gemini_api_key_here":
    print("[bold green]✓ GEMINI_API_KEY loaded successfully from .env![/bold green]")
else:
    print("[bold red]✗ GEMINI_API_KEY is missing or invalid in .env![/bold red]")