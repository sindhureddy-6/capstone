from google.adk.agents import LlmAgent
from ..utils import GEMINI_MODEL,STATE_COPING_STRATEGY
from google.adk.tools import google_search
from google.adk.tools.tool_context import ToolContext
from google.adk.planners import PlanReActPlanner
from google.adk.tools.agent_tool import AgentTool

def approve_strategy(tool_context: ToolContext):
    print(f"[Tool Call] approve_strategy triggered")
    tool_context.actions.escalate = True
    return {}

search_agent = LlmAgent(
    name="search_agent",
    model=GEMINI_MODEL,
    instruction="""
You are a focused web search assistant.
Given a search query, return ONLY high-quality mental health techniques *from HelpGuide.org*.
Examples: breathing exercises, grounding, progressive muscle relaxation.
""",
    output_key="search_results",
)
search_tool = AgentTool(agent=search_agent)

strategy_refiner = LlmAgent(
    name="strategy_refiner",
    model=GEMINI_MODEL,
    instruction=f"""
You are the final optimizer. If the previous strategy has issues (from QualityChecker feedback), fix it.

Rules:
- You may (and should) use `search_tool` again with "site:helpguide.org ..." to find a better technique if needed.
- Fix ALL problems mentioned (personalization, length, past failures, etc.).
- If feedback says "Coping strategy approved.", immediately call the `approve_strategy` tool and output nothing else.
- Otherwise, output ONLY the improved 50–100 word strategy, sourced from HelpGuide.org.

Example search if needed: "site:helpguide.org grounding techniques OR sensory strategies"
""",
    tools=[search_tool, approve_strategy],  
    description="Refines the strategy or approves if perfect.",
    output_key=STATE_COPING_STRATEGY
)