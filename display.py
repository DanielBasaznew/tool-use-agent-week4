"""
Renders the structured ResearchReport beautifully in the terminal using Rich.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from models import ResearchReport

def display_report(report: ResearchReport):
    console = Console()
    
    # 1. Print the summary inside a nice bordered panel
    console.print(Panel(report.summary, title="Research Summary", border_style="bold blue"))
    
    # 2. Print the bullet points
    console.print("\n[bold green]Key Findings:[/bold green]")
    for finding in report.key_findings:
        console.print(f"• {finding}")
        
    # 3. Create and populate the Citations Table
    table = Table(title="Sources & Citations", style="cyan")
    table.add_column("Source Title", style="cyan", overflow="fold")
    table.add_column("Cited Fact / Key Point", style="white", overflow="fold")
    
    for s in report.sources:
        # Slicing the strings [:50] keeps the terminal table from breaking formatting on long text
        table.add_row(s.title[:50], s.key_point[:70])
        
    console.print("\n")
    console.print(table)
    
    # 4. Print the self-assessed confidence score
    console.print(f"\n[bold magenta]Agent Confidence Score:[/bold magenta] {report.confidence.upper()}\n")