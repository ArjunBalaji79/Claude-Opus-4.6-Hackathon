from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel
from datetime import datetime
import anthropic
import json
import re


class AgentOutput(BaseModel):
    agent_name: str
    output_type: str
    data: dict
    confidence: float
    sources: list[str]
    reasoning: str
    timestamp: datetime


class BaseAgent(ABC):
    def __init__(self, client: anthropic.Anthropic):
        self.client = client
        self.agent_name = self.__class__.__name__
        self.model = "claude-opus-4-6"

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def format_input(self, raw_input: Any) -> list[dict]:
        pass

    @abstractmethod
    def parse_output(self, response: str) -> AgentOutput:
        pass

    async def process(self, raw_input: Any) -> AgentOutput:
        messages = self.format_input(raw_input)
        try:
            # Run the synchronous Anthropic call in a thread so it doesn't block the event loop
            import asyncio
            import functools
            response = await asyncio.to_thread(
                functools.partial(
                    self.client.messages.create,
                    model=self.model,
                    max_tokens=4096,
                    system=self.get_system_prompt(),
                    messages=messages
                )
            )
            return self.parse_output(response.content[0].text)
        except Exception as e:
            # Graceful fallback: return realistic mock data for demo
            print(f"[{self.agent_name}] API error: {e} — using demo fallback")
            return self.get_fallback_output(raw_input)

    def get_fallback_output(self, raw_input: Any) -> AgentOutput:
        """Override in subclasses to provide realistic demo fallback data."""
        return AgentOutput(
            agent_name=self.agent_name,
            output_type="fallback",
            data={"error": "API unavailable", "demo_mode": True},
            confidence=0.5,
            sources=[],
            reasoning="Demo fallback — check ANTHROPIC_API_KEY in backend/.env",
            timestamp=datetime.utcnow()
        )

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from response text, handling markdown code blocks and minor syntax errors."""
        # 1. Try code block first
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if match:
            candidate = match.group(1).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

        # 2. Try whole text
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass

        # 3. Find the first complete JSON object by bracket counting
        start = text.find('{')
        if start != -1:
            depth = 0
            for i, ch in enumerate(text[start:], start):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        candidate = text[start:i + 1]
                        try:
                            return json.loads(candidate)
                        except json.JSONDecodeError:
                            # Strip trailing commas (common Claude mistake)
                            cleaned = re.sub(r',\s*([}\]])', r'\1', candidate)
                            try:
                                return json.loads(cleaned)
                            except json.JSONDecodeError:
                                break

        raise ValueError(f"Could not extract JSON from response: {text[:200]}")
