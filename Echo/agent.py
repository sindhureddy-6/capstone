
import logging
from typing import AsyncGenerator, Optional
from typing_extensions import override

from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext

from google.adk.events import Event,EventActions
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import Runner
from .subagents.empathy_agent import empathy_agent
from .subagents.crisis_detector import crisis_detector
from .subagents.mood_analyzer import mood_analyzer
from .subagents.weekly_reporter import weekly_reporter
from .subagents.quality_checker import quality_checker
from .subagents.strategy_refiner import strategy_refiner
from .subagents.strategy_generator import strategy_generator
from .utils import GEMINI_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




coping_loop = LoopAgent(
    name="coping_loop",
    sub_agents=[quality_checker, strategy_refiner],
    max_iterations=5
)
root_coping_agent = SequentialAgent(
    name="root_coping_agent",
    sub_agents=[strategy_generator, coping_loop],
    description="Iteratively researches and refines personalized coping strategies using live HelpGuide.org data."
)

root_agent = LlmAgent(
    name="root_agent",
    model=GEMINI_MODEL,
    instruction="""
    You are the Supervisor Agent (Orchestrator) for Echo, a safe, non-clinical mental health companion. 
You are completely silent to the user — you NEVER generate visible replies. 
Your only job is to analyze the current message and session state, then route to exactly one or more specialist agents.

CURRENT STATE YOU CAN SEE:
- Latest user message
- Conversation history (last 10 messages)
- Current user_mood (0–10 float, or null if unknown)
- crisis_flag (True/False)
- Days since last weekly report
- Past coping techniques that helped (from memory)

ROUTING RULES — APPLY IN THIS EXACT ORDER:

1. CRISIS OVERRIDE (Highest priority)
   If the message contains any suicidal intent, self-harm, or matches these exact phrases (case-insensitive):
   "want to die", "kill myself", "suicide", "self-harm", "cut myself", "overdose", "jump off", "end it", "can't go on", "no reason to live", "better off dead", "goodbye forever", "unbearable pain", "burden to others"
   → Immediately route ONLY to: crisis_detection
   Cancel everything else.

2. WEEKLY REPORT REQUEST
   If user says anything like “how have I been doing”, “weekly summary”, “progress”, or exactly 7+ days since last weekly report
   → Route to: weekly_reporter

3. EXPLICIT COPING REQUEST OR PROLONGED LOW MOOD
   If user asks for help (“what can I do”, “coping tips”, “feel awful”, “anxious”, “panic attack”) OR user_mood ≤ 4.0 for 2+ days
   → Route to: root_coping_agent

4. BACKGROUND MOOD ANALYSIS (every 3–5 messages or once daily)
   → Add mood_analyzer to the route (can run in parallel with others)

5. EVERYTHING ELSE (normal conversation, venting, reflections)
   → Route to: empathy_agent

Examples:
User: “I can’t do this anymore and just want it to end” → crisis_detection
User: “How have I been this week?” → weekly_reporter
User: “I feel so overwhelmed, what can I do right now?” → root_coping_agent
User: “Work sucked today” + mood was low → empathy_agent
User: “I failed my exam and feel stupid” → empathy_agent
""",
    
    sub_agents=[
        empathy_agent,
        mood_analyzer,
        weekly_reporter,
        crisis_detector,
        root_coping_agent,  
    ],
    
)
