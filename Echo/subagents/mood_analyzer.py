from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from ..utils import GEMINI_MODEL

def mood_instruction(ctx: InvocationContext) -> str:
    return "Analyze the user's mood from their message on a scale of 0-10 (0=worst, 10=best). Output ONLY the number."

mood_analyzer = LlmAgent(
    name="mood_analyzer",
    model=GEMINI_MODEL,
    instruction=mood_instruction,
    output_key="user_mood",
)