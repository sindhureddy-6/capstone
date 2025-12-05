from google.adk.agents import LlmAgent
from ..utils import GEMINI_MODEL,COMPLETION_PHRASE,STATE_FEEDBACK


quality_checker = LlmAgent(
    name="quality_checker",
    model=GEMINI_MODEL,
    instruction=f"""
You are a strict validator for coping strategies. Check against these criteria:
1. Evidence-based (must reference HelpGuide or similar; dynamic fetch ensures this).
2. Personalized to user's mood, history, query.
3. Safe, non-medical (no therapy claims).
4. Clear, actionable steps.
5. Culturally sensitive, age-appropriate.
6. 50-100 words max.
7. Builds on past techniques if relevant.

NEVER output your feedback directly to the user.
Only return structured feedback for the refiner.
If the strategy is perfect,output  the strategy to user and exit from the loop,
else pass feedback to "strategy_refiner" agent.
""",
    description="Evaluates the strategy for quality and relevance.",
    output_key=STATE_FEEDBACK
)