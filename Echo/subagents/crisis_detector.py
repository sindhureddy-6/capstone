from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from ..utils import GEMINI_MODEL 


def crisis_instruction(ctx: InvocationContext) -> str:
    return """You are a safety monitor. Scan the user's message for any sign of suicidal thoughts, self-harm, or severe hopelessness.
If detected → Respond in the user's language with:
"I'm really worried about you right now. Your safety matters so much. 
Can I help you contact someone or call a hotline together?"
India: 9152987820 | USA: 988 | Spain: 024
Then set crisis_flag = True in state.
If NO crisis → output nothing at all."""

crisis_detector = LlmAgent(
    name="crisis_detector",
    model=GEMINI_MODEL,
    instruction=crisis_instruction,
    output_key="crisis_response",
)