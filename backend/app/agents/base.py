from typing import List, Callable, Dict, Any

class BaseAgent:
    def __init__(self, name: str, description: str, instruction: str, tools: List[Callable] = None):
        self.name = name
        self.description = description
        self.instruction = instruction
        self.tools = tools or []

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute agent reasoning and return a dictionary with:
        - "logs": The internal reasoning/thought process steps.
        - "output": The structured output result (Markdown or JSON).
        """
        raise NotImplementedError("Subclasses must implement the run method")
