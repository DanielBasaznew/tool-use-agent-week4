"""
Data models for the Citation Engine using Pydantic.
"""

from typing import List
from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str = Field(description="The title of the source document or webpage.")
    url: str = Field(description="The exact URL where this information was found.")
    key_point: str = Field(description="The specific fact or claim attributed to this source.")


class ResearchReport(BaseModel):
    summary: str = Field(description="A 2-3 paragraph comprehensive answer to the user query.")
    key_findings: List[str] = Field(description="Bullet-point list of critical takeaways.")
    sources: List[Source] = Field(description="List of cited sources backing up the report.")
    confidence: str = Field(description="Self-assessment of research reliability: 'high', 'medium', or 'low'.")