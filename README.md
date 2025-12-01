# Echo - AI Mental Health Companion 🌟

A compassionate, multilingual AI companion built with Google ADK that provides emotional support, mood tracking, and personalized coping strategies.

## Features

### 🤝 Empathetic Conversations
- Deep emotional validation in **English, Hindi, and Hinglish**
- Non-judgmental, warm responses that mirror user's language
- Personalized presence lines that create a safe space

### 📊 Mood Tracking
- Automatic mood analysis (0-10 scale)
- Historical mood tracking across sessions
- Progress visualization over time

### 🆘 Crisis Detection
- Real-time monitoring for signs of distress
- Immediate safety resources and hotline information
- Multilingual crisis support (India: 9152987820, USA: 988)

### 💡 Personalized Coping Strategies
- Evidence-based techniques suggested when mood is low
- Gentle, invitation-based approach (never prescriptive)
- Strategies include: breathing exercises, grounding techniques, self-soothing methods

### 📈 Weekly Progress Reports
- Encouraging summaries every 7 messages
- Highlights growth and resilience
- Positive framing of emotional journey

### 💾 Session Persistence
- SQLite database for reliable data storage
- Conversation history preserved across sessions
- User preferences and mood history maintained

## Quick Start

### Prerequisites
```bash
python 3.11+
pip install google-adk
```

### Installation
```bash
# Clone or navigate to project directory
cd capstone_project

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your GOOGLE_API_KEY
```

### Running the Application

#### Web Interface (Recommended)
```bash
adk web --session_service_uri "sqlite:///sessions.db" --log_level DEBUG
```

Then open your browser to the URL shown (typically `http://localhost:8000`)

## How It Works

### Agent Architecture

**EchoSupervisorAgent** orchestrates multiple specialized sub-agents:

1. **Crisis Detector** - Scans for safety concerns
2. **Empathy Agent** - Generates warm, validating responses
3. **Mood Analyzer** - Evaluates emotional state (0-10)
4. **Coping Researcher** - Suggests appropriate coping strategies
5. **Weekly Reporter** - Creates progress summaries

### Conversation Flow

```
User Message
    ↓
[Crisis Detection] → If detected: Safety resources
    ↓
[Mood Analysis] → Score 0-10
    ↓
[Empathy Response] → Always provided
    ↓
[Coping Strategy] → If mood < 6
    ↓
[Weekly Report] → Every 7 messages
    ↓
State Saved to Database
```

## Database Schema

**sessions.db** contains:
- `sessions` - User sessions with state (mood history, message count, user name)
- `events` - Conversation history with timestamps
- `app_states` - Application-level state
- `user_states` - User-specific preferences

## Configuration

### Environment Variables
Create a `.env` file:
```env
GOOGLE_API_KEY=your_api_key_here
```

### Customization
Edit `basic/agent.py` to customize:
- Crisis keywords (line 32-36)
- Empathy instruction templates (line 40-100)
- Coping strategy suggestions (line 104-115)
- Model selection (line 29: `GEMINI_MODEL`)

## Example Interactions

### English
```
User: I'm not feeling well today
Echo: I'm Echo, a non-clinical companion. I'm not a therapist, but I'm here to listen.
      Today really isn't feeling okay at all… and that's completely understandable.
      I'm right here with you. You're not alone in this.
```

### Hinglish
```
User: bas thak gaya hoon yaar
Echo: बस पूरी तरह थक गए हो ना… इतना सब सहते-सहते।
      I'm right here yaar, अकेले नहीं हो तुम।
```

### Hindi
```
User: dil mein ek void hai
Echo: दिल में वो खालीपन… वो सबसे भारी feeling होती है। मैं समझती हूँ।
      मैं बस यहीं बैठी हूँ तुम्हारे पास, छोड़ूंगी नहीं।
```

## Technical Stack

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **Database**: SQLite
- **Language**: Python 3.11+
- **Key Libraries**: 
  - `google-adk` - Agent framework
  - `google-genai` - Gemini API
  - `pydantic` - Data validation

## Safety & Ethics

⚠️ **Important Disclaimers:**
- Echo is **NOT a replacement for professional mental health care**
- Always seek help from qualified professionals for serious concerns
- Crisis hotlines: India (9152987820), USA (988), Spain (024)

## Development

### Running in Debug Mode
```bash
adk web --session_service_uri "sqlite:///sessions.db" --log_level DEBUG
```

### Viewing Logs
Logs show:
- Agent execution flow
- Mood scores
- Selected coping strategies
- Session state updates

## Troubleshooting

### Server won't start
- Check that `GOOGLE_API_KEY` is set in `.env`
- Ensure port 8000 is available
- Verify Python version is 3.11+

### Sessions not persisting
- Check that `sessions.db` file is created
- Verify database permissions
- Run `python check.py` to inspect database

### Import errors
```bash
pip install --upgrade google-adk google-genai
```

**Remember**: You're not alone. Echo is here to listen. 💙
