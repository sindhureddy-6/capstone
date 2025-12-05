from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from ..utils import GEMINI_MODEL

def weekly_instruction(ctx: InvocationContext) -> str:
    moods = ctx.state.get("past_moods", [])
    return f"""You are a gentle growth guide. Summarize the user's emotional week positively.
Use {moods} array. Never judge.
Example: "This week you reached out 4 times when things felt hard — that's real strength.
Your average mood rose from 4.1 to 5.4. You're growing, even when it doesn't feel like it."
Respond in user's language. """

weekly_reporter = LlmAgent(
    name="weekly_reporter",
    model=GEMINI_MODEL,
    instruction=weekly_instruction,
    output_key="weekly_report",
)