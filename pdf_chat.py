"""
Interactive PDF Q&A Session (Week 4, Day 4)
Pre-loads a PDF overview into context and allows the user to chat with the document.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools.pdf_reader import read_pdf, read_pdf_page

# Load environment variables (API Key) from .env file
load_dotenv()


def run_pdf_chat():
    print("=== Welcome to PDF Document Q&A ===")
    pdf_path = input("Enter the path to your PDF file (e.g., sample.pdf): ").strip()

    if not os.path.exists(pdf_path):
        print("Error: File not found. Please check the path and try again.")
        return

    print(f"\n[Extracting overview from '{os.path.basename(pdf_path)}'...]")
    
    # 1. Pre-load the document overview using our tool
    pdf_overview = read_pdf(pdf_path)
    
    # Initialize the Gemini Client
    client = genai.Client()
    
    # 2. Inject the extracted text directly into the system instructions
    system_instruction = (
        "You are an expert document analysis assistant. You have been provided with the overview of a PDF document below. "
        "Answer the user's questions based strictly on this document. "
        "If the answer requires details from a specific page (especially if the overview was truncated), "
        "you MUST use the `read_pdf_page` tool to fetch that page's full text before answering.\n\n"
        f"--- START DOCUMENT OVERVIEW ---\n{pdf_overview}\n--- END DOCUMENT OVERVIEW ---"
    )

    # 3. Give the agent access to the page-fetching tool
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[read_pdf_page], 
        temperature=0.2
    )

    # 4. Start the interactive chat session
    chat = client.chats.create(model="gemini-3.1-flash-lite", config=config)
    
    print("\n[Overview Loaded! You can now chat with your PDF. Type 'quit' to exit.]")
    print("-" * 50)

    while True:
        user_input = input("\nYou ask question or Type 'quit' to exit.: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Exiting PDF Q&A. Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        print("\nAgent is thinking...")
        try:
            response = chat.send_message(user_input)
            print(f"\nAgent: {response.text}")
        except Exception as e:
            print(f"\n[Error communicating with Gemini: {e}]")

if __name__ == "__main__":
    run_pdf_chat()