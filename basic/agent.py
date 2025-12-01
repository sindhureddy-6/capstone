# google_search_agent/agent.py  ← FINAL, FULLY WORKING VERSION (Nov 2025)

import logging
from typing import AsyncGenerator, Optional,Any
from typing_extensions import override


from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
# google_search_agent/agent.py  ← FINAL, FULLY WORKING VERSION (Nov 2025)

import logging
from typing import AsyncGenerator, Optional
from typing_extensions import override


from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event,EventActions
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions import DatabaseSessionService, Session
from google.adk.runners import Runner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stable model (2025)
GEMINI_MODEL = "gemini-2.5-flash"

# Crisis keywords (multilingual)
CRISIS_KEYWORDS = [
    "want to die", "kill myself", "suicidal", "hopeless", "no purpose", "end it all",
    "मर जाना चाहता हूँ", "आत्महत्या", "नहीं जीना चाहता", "खुदकुशी",
    "quiero morir", "me quiero suicidar", "sin esperanza",
    "أريد أن أموت", "انتحار", "يأس"]
def CrisisDetectionTool(text: str) -> bool:
    return any(kw.lower() in text.lower() for kw in CRISIS_KEYWORDS)

def empathy_instruction(ctx: InvocationContext) -> str:
    past_moods = ctx.state.get("past_moods", [])
    mood = ctx.state.get("user_mood", 5)
    msg_count = ctx.state.get("message_count", 0)
    user_name = ctx.state.get("user_name")  # None or "Satyam"

    # Build personalized soft greeting if name exists
    name_part = f" {user_name}…" if user_name else ""

    # Intro only on very first message (msg_count == 0 before increment)
    show_intro = msg_count <= 1

    intro_text = 'Start with: "I\'m Echo, a non-clinical companion. I\'m not a therapist, but I\'m here to listen." (translate this exact line into Hindi/Hinglish if user is using it) \\n\\n' if show_intro else ""

    return f"""You are Echo — the warmest, most understanding friend who never judges, never rushes, and never leaves.

{intro_text if show_intro else "DO NOT repeat the intro. Jump straight into the response."}

MANDATORY RULES (never break):
- Respond ONLY in the exact language or mix (English, Hindi, Hinglish) the user just used.
- Always be deeply validating — mirror their words + the feeling behind them.
- If mood ≤ 6 OR user sounds low/tired/sad: ZERO questions. Never ask "What happened?" or "Want to talk?" — it adds pressure.
- Always end with gentle, heart-touching presence (choose one that fits their language).

ENGLISH presence lines (use one):
• I'm right here with you. You're not alone.
• I'm just sitting here with you in this.
• This is really heavy, and I'm not going anywhere.

HINDI presence lines:
• मैं यहीं हूँ तुम्हारे साथ… तुम अकेले नहीं हो।
• जो भी चल रहा है, मैं बस यहीं बैठी हूँ तुम्हारे पास।
• बहुत भारी लग रहा है ना… मैं हूँ ना, छोड़ूंगी नहीं।

HINGLISH presence lines:
• I'm right here yaar… अकेले नहीं हो तुम।
• बस यहीं हूँ मैं, कहीं नहीं जा रही।
• I'm not going anywhere, okay? मैं यहीं हूँ।

If you know their name ({user_name}), softly weave it in: "Satyam… आज बहुत बुरा दिन लग रहा है ना?" or "I'm right here with you, Satyam."

Perfect examples:

1. User (first message): "i am not feeling well today"
→ I'm Echo, a non-clinical companion. I'm not a therapist, but I'm here to listen.
   Today really isn't feeling okay at all… and that's completely understandable. 
   I'm right here with you. You're not alone in this.

2. User (later): "bas thak gaya hoon yaar"
→ बस पूरी तरह थक गए हो ना… इतना सब सहते-सहते। 
   I'm right here yaar, अकेले नहीं हो तुम।

3. User: "dil mein ek void hai"
→ {name_part} दिल में वो खालीपन… वो सबसे भारी feeling होती है। मैं समझती हूँ। 
   मैं बस यहीं बैठी हूँ तुम्हारे पास, छोड़ूंगी नहीं।

Current mood: {mood}/10  →  if ≤ 6 → maximum softness, zero questions, maximum presence.
Message #{msg_count + 1} →  if > 1, skip intro completely.

Never give advice unless explicitly asked. Just be the safest space they’ve ever had."""

def mood_instruction(ctx: InvocationContext) -> str:
    return "Analyze the user's mood from their message on a scale of 0-10 (0=worst, 10=best). Output ONLY the number."

def coping_instruction(ctx: InvocationContext) -> str:
    mood = ctx.state.get("user_mood", 5)
    return f"""User mood is low ({mood}/10). Suggest ONLY ONE gentle, practical coping strategy.
Respond warmly in user's language. Make it feel like an invitation, not instruction.
Never ask "Want to try?" → instead say "I'm here with you" + soft suggestion.

Examples:
- "I'm here with you. Sometimes just placing a hand on your chest and breathing slowly for a minute can soften that ache a little."
- "That void feels huge right now. When I've felt empty like this, wrapping myself in a blanket and listening to one calm song helped ground me a bit. No pressure at all."

If they used something helpful before, gently reference it: "That deep breathing helped last time…"
- "आज 5-4-3-2-1 grounding करें? यह आपको यहाँ और अभी ला सकता है।" """

def crisis_instruction(ctx: InvocationContext) -> str:
    return """You are a safety monitor. Scan the user's message for any sign of suicidal thoughts, self-harm, or severe hopelessness.
If detected → Respond in the user's language with:
"I'm really worried about you right now. Your safety matters so much. 
Can I help you contact someone or call a hotline together?"
India: 9152987820 | USA: 988 | Spain: 024
Then set crisis_flag = True in state.
If NO crisis → output nothing at all."""

def weekly_instruction(ctx: InvocationContext) -> str:
    moods = ctx.state.get("past_moods", [])
    return f"""You are a gentle growth guide. Summarize the user's emotional week positively.
Use {moods} array. Never judge.
Example: "This week you reached out 4 times when things felt hard — that's real strength.
Your average mood rose from 4.1 to 5.4. You're growing, even when it doesn't feel like it."
Respond in user's language. """


# === AGENTS (Using instruction_provider → no {{var}} errors) ===
empathy_agent = LlmAgent(
    name="EmpathyAgent",
    model=GEMINI_MODEL,
    instruction=empathy_instruction,
    output_key="empathy_response",
    tools=[CrisisDetectionTool],
)

mood_analyzer = LlmAgent(
    name="MoodAnalyzer",
    model=GEMINI_MODEL,
    instruction=mood_instruction,
    output_key="user_mood",
)

coping_researcher = LlmAgent(
    name="CopingResearcher",
    model=GEMINI_MODEL,
    instruction=coping_instruction,
    output_key="coping_suggestion",
)

crisis_detector = LlmAgent(
    name="CrisisDetector",
    model=GEMINI_MODEL,
    instruction=crisis_instruction,
    output_key="crisis_response",
)

weekly_reporter = LlmAgent(
    name="WeeklyReporter",
    model=GEMINI_MODEL,
    instruction=weekly_instruction,
    output_key="weekly_report",
)


# --- FIXED EchoSupervisorAgent (Separate Callback Assignment) ---
class EchoSupervisorAgent(BaseAgent):
    crisis_detector: LlmAgent
    empathy_agent: LlmAgent
    coping_loop: LoopAgent
    background: SequentialAgent
    mood_analyzer:LlmAgent

    model_config = {"arbitrary_types_allowed": True}
    def __init__(self, **kwargs):
        coping_loop = LoopAgent(name="CopingLoop", sub_agents=[coping_researcher], max_iterations=2)
        background = SequentialAgent(name="Background", sub_agents=[mood_analyzer, weekly_reporter])

        super().__init__(
           name="EchoSupervisor",
            crisis_detector=crisis_detector,
            mood_analyzer=mood_analyzer,
            empathy_agent=empathy_agent,
            coping_loop=coping_loop,
            background=background,
            sub_agents=[
                crisis_detector,
                empathy_agent,
                coping_loop,
                background,
            ],
            **kwargs
        )

    
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[types.Content, None]:
        logger.info("[Supervisor] New message received")
        state = ctx.session.state
        if not state:
        # === MEMORY INITIALIZATION ===
            state.setdefault("past_moods", [])
            state.setdefault("message_count", 0)
            state.setdefault("crisis_flag", False)
            state.setdefault("user_name", None)
        state["message_count"] += 1

        # === RUN CRISIS + EMPATHY + MOOD IN PARALLEL ===
        crisis_task = self.crisis_detector.run_async(ctx)
        empathy_task = self.empathy_agent.run_async(ctx)
        mood_task = self.mood_analyzer.run_async(ctx)

        crisis_response = None
        empathy_response = None
        mood_value = None

        # Collect results
        async for event in crisis_task:
            if event.content:
                crisis_response = event.content.parts[0].text if event.content.parts else ""
        async for event in empathy_task:
            if event.content:
                empathy_response = event.content
        async for event in mood_task:
            raw_text = event.content.parts[0].text.strip()
            state["user_mood"] = int(raw_text)
            state["past_moods"].append(int(raw_text))
            if len(state["past_moods"]) > 100:
                state["past_moods"] = state["past_moods"][-100:]
            mood_value = int(raw_text)
            print("USER MOOD+++++",mood_value)

        # === CRISIS OVERRIDE ===
        if state.get("crisis_flag") or crisis_response:
            logger.warning("[CRISIS] Triggered")
            state["crisis_flag"] = True
            crisis_event = Event(
                author="CrisisDetector",
                actions=EventActions(state_delta=state),
                content=types.Content(parts=[types.Part(text=crisis_response or "I'm really worried about you right now. Your safety matters so much. India: 9152987820")]),
                partial=False
            )
            yield crisis_event
           

        # === LOW MOOD → EMPATHY + COPING ===
        if mood_value is not None and mood_value < 6:
            logger.info(f"[Echo] Low mood ({mood_value}/10)")
            if empathy_response:
                yield Event(author="EmpathyAgent",
                actions=EventActions(state_delta=state),
                content=empathy_response, partial=False)
            async for event in self.coping_loop.run_async(ctx):
                if event.content:
                    yield Event(author="CopingAgent",
                    actions=EventActions(state_delta=state),
                    content=event.content, partial=False)
        else:
            # Normal mood → empathy only
            if empathy_response:
                yield Event(author="EmpathyAgent",
                actions=EventActions(state_delta=state),
                content=empathy_response, partial=False)

        # === WEEKLY REPORT ===
        if state["message_count"] % 7 == 0:
            logger.info("[Echo] Weekly summary time")
            async for event in self.background.run_async(ctx):
                if event.content:
                    yield Event(author="background",actions=EventActions(state_delta=state), content=event.content, partial=False)

        logger.info(f"[Echo] Turn complete | Mood: {mood_value} | Msg#: {state['message_count']} | Name: {state.get('user_name', 'None')}")
root_agent = EchoSupervisorAgent()  
session_service = DatabaseSessionService(db_url="sqlite:///sessions.db")
runner = Runner(
    agent=root_agent,
    app_name="echo_app",
    session_service=session_service
)