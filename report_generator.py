"""
Converts raw gathered research into a structured, cited Pydantic model.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from models import ResearchReport

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_research_report(question: str, gathered_info: str) -> ResearchReport:
    """Take raw gathered info and format it into a cited research report."""
    
    prompt = f"Question: {question}\n\nGathered information:\n{gathered_info}\n\nCreate a structured report with citations."
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", # Using the model we know works for your API key
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a research assistant. Create a structured report with proper citations using ONLY the information provided.",
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=ResearchReport, # This forces Gemini to output the Pydantic structure!
        ),
    )
    
    # The new google-genai SDK automatically parses the JSON into your Pydantic model
    return response.parsed