# Echo - AI Mental Health Companion 🌿

Echo is a compassionate, non-clinical mental health companion built with Google's Agent Development Kit (ADK). It uses a multi-agent architecture to provide empathetic support, mood tracking, crisis detection, and personalized coping strategies.

## 🎯 Overview

Echo is designed to be a safe, supportive AI companion that:
- Listens with empathy and validates emotions
- Tracks mood patterns over time
- Detects crisis situations and provides emergency resources
- Generates evidence-based coping strategies from HelpGuide.org
- Provides weekly progress reports

**⚠️ Important Disclaimer**: Echo is NOT a replacement for professional mental health care. It's an AI companion designed to provide support and resources, not clinical treatment.

## 🏗️ Architecture

Echo uses a sophisticated multi-agent system with the following components:

### Root Agent (Orchestrator)
The supervisor agent that routes user messages to appropriate specialist agents based on:
- Crisis detection keywords
- User mood levels
- Explicit coping requests
- Weekly report requests
- General conversation needs

### Specialist Agents

#### 1. **Empathy Agent** (`empathy_agent.py`)
- Primary conversational interface
- Uses reflective listening and emotional validation
- Provides warm, compassionate responses
- Includes multilingual crisis keyword detection

#### 2. **Mood Analyzer** (`mood_analyzer.py`)
- Analyzes user messages to determine mood on a 0-10 scale
- Runs periodically to track emotional trends
- Stores mood data for weekly reports

#### 3. **Crisis Detector** (`crisis_detector.py`)
- Monitors for suicidal thoughts, self-harm, or severe distress
- Provides immediate safety resources and hotline numbers
- Supports multiple countries (India: 9152987820, USA: 988, Spain: 024)

#### 4. **Weekly Reporter** (`weekly_reporter.py`)
- Generates compassionate weekly summaries
- Highlights emotional growth and patterns
- Uses stored mood data to show progress

#### 5. **Coping Strategy System** (Multi-agent loop)
A sophisticated iterative refinement system consisting of:

- **Strategy Generator** (`strategy_generator.py`)
  - Searches HelpGuide.org for evidence-based techniques
  - Generates personalized coping strategies (100-200 words)
  - Uses Google Search to fetch live content

- **Quality Checker** (`quality_checker.py`)
  - Validates strategies against 7 quality criteria
  - Ensures evidence-based, personalized, safe content
  - Provides structured feedback for refinement

- **Strategy Refiner** (`strategy_refiner.py`)
  - Improves strategies based on quality feedback
  - Can perform additional searches if needed
  - Approves and exits loop when strategy is perfect

- **Coping Loop** (LoopAgent)
  - Iterates between Quality Checker and Strategy Refiner
  - Maximum 5 iterations to ensure quality
  - Escalates when strategy is approved

## 📁 Project Structure

```
capstone_project/
├── Echo/
│   ├── __init__.py
│   ├── agent.py              # Root orchestrator agent
│   ├── utils.py              # Shared constants and utilities
│   └── subagents/
│       ├── empathy_agent.py
│       ├── mood_analyzer.py
│       ├── crisis_detector.py
│       ├── weekly_reporter.py
│       ├── strategy_generator.py
│       ├── quality_checker.py
│       └── strategy_refiner.py
├── main.py
├── pyproject.toml
├── uv.lock
├── .env
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Google ADK 1.11.0
- Google API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd capstone_project
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install google-adk==1.11.0
   ```
   
   Or using `uv`:
   ```bash
   uv sync
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running Echo

#### Using ADK Web Interface
```bash
adk web Echo.agent:root_agent
```

#### Using ADK CLI
```bash
adk run Echo.agent:root_agent
```

## 🔧 Configuration

### Model Configuration
The default model is `gemini-2.5-flash-lite`, configured in `Echo/utils.py`:
```python
GEMINI_MODEL = "gemini-2.5-flash-lite"
```

### State Keys
Echo uses the following state keys for inter-agent communication:
- `user_context` - User's current context and history
- `coping_strategy` - Generated coping strategy
- `feedback` - Quality checker feedback
- `user_mood` - Current mood score (0-10)
- `crisis_response` - Crisis detection output
- `empathy_response` - Empathy agent output
- `weekly_report` - Weekly summary output

## 🔄 Agent Routing Logic

The root agent follows this priority order:

1. **Crisis Override** (Highest Priority)
   - Detects suicidal intent, self-harm keywords
   - Routes to `crisis_detector` immediately

2. **Weekly Report Request**
   - User asks for progress/summary
   - 7+ days since last report
   - Routes to `weekly_reporter`

3. **Coping Request**
   - User explicitly asks for help
   - Mood ≤ 4.0 for 2+ days
   - Routes to `root_coping_agent` (strategy system)

4. **Background Mood Analysis**
   - Runs every 3-5 messages
   - Routes to `mood_analyzer`

5. **Default Conversation**
   - Normal venting, reflections
   - Routes to `empathy_agent`

## 🛠️ Development

### Adding New Agents

1. Create a new file in `Echo/subagents/`
2. Define your agent using `LlmAgent`:
   ```python
   from google.adk.agents import LlmAgent
   from ..utils import GEMINI_MODEL
   
   my_agent = LlmAgent(
       name="my_agent",
       model=GEMINI_MODEL,
       instruction="Your instruction here",
       output_key="my_output"
   )
   ```
3. Import and add to `root_agent.sub_agents` in `agent.py`
4. Update routing logic in root agent instruction

### Testing

Test individual agents:
```bash
adk run Echo.subagents.empathy_agent:empathy_agent
```

## ⚠️ Known Issues

1. **Missing Import**: `agent.py` imports `coping_researcher` which doesn't exist in the codebase. This import should be removed or the file should be created.

## 🌍 Multilingual Support

Echo includes crisis detection in multiple languages:
- **English**: "want to die", "kill myself", "suicidal"
- **Hindi**: "मर जाना चाहता हूँ", "आत्महत्या"
- **Spanish**: "quiero morir", "me quiero suicidar"
- **Arabic**: "أريد أن أموت", "انتحار"

## 📊 Features in Detail

### Evidence-Based Coping Strategies
- All strategies sourced from HelpGuide.org
- Personalized based on:
  - Current mood level
  - Energy level
  - Past techniques that didn't work
  - User's current environment (work/school/home)

### Quality Assurance
Strategies are validated against:
1. Evidence-based sources
2. Personalization to user context
3. Safety (non-medical, no therapy claims)
4. Clear, actionable steps
5. Cultural sensitivity
6. Appropriate length (50-100 words)
7. Builds on past techniques

### Crisis Support
Provides immediate resources for:
- Suicidal thoughts
- Self-harm ideation
- Severe hopelessness
- Emergency situations



- **India**: 9152987820 (iCall Psychosocial Helpline)
- **USA**: 988 (Suicide & Crisis Lifeline)
- **Spain**: 024 (Línea de Atención a la Conducta Suicida)
- **International**: https://findahelpline.com


## 🙏 Acknowledgments

- Built with [Google ADK](https://github.com/google/adk)
- Evidence-based content from [HelpGuide.org](https://www.helpguide.org)
- Gemini 2.5 Flash Lite model

---

**Remember**: Echo is a companion, not a therapist. Always seek professional help for serious mental health concerns.
