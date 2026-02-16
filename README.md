# CrisisCore

**Multimodal, Multi-Agent Disaster Response Coordination with Epistemic Transparency**

> When a 6.8 earthquake hits, contradictory reports flood in simultaneously. A satellite shows a bridge intact. A first-responder says it collapsed. Social media is hysterical. CrisisCore uses 6 specialized Claude agents to process the chaos, surface the contradictions, and let human operators make auditable decisions with explicit tradeoffs.

Built with **Claude Opus 4.6** for the Anthropic Hackathon.

---

## The Core Insight

Most disaster AI hides uncertainty. CrisisCore **surfaces it**.

When agents disagree, the system doesn't pick a winner — it shows the disagreement, lets agents debate it live, and gives the human operator everything they need to decide.

---

## How It Works

```mermaid
flowchart LR
    subgraph Signals["Incoming Signals"]
        IMG["🛰 Drone/Satellite\nImages"]
        AUD["📻 911 Calls\nRadio Dispatches"]
        TXT["📱 Social Media\nOfficial Reports"]
    end

    subgraph Agents["Claude Agents"]
        VA["VisionAgent\n(damage assessment)"]
        AA["AudioAgent\n(transcript analysis)"]
        TA["TextAgent\n(credibility scoring)"]
    end

    IMG --> VA
    AUD --> AA
    TXT --> TA

    subgraph Graph["Situation Graph"]
        INC["Incidents\n+ confidence scores"]
        CON["Contradictions\ndetected across sources"]
        ACT["Action Recommendations\nwith explicit tradeoffs"]
    end

    VA --> INC
    AA --> INC
    TA --> INC

    INC --> VER["VerificationAgent\n(cross-source check)"]
    VER -->|"sources disagree"| CON
    INC --> PL["PlanningAgent\n(resource allocation)"]
    PL --> ACT

    subgraph Human["Human Decisions"]
        DEB["Debate Room\n4 agents argue live"]
        APP["Approve / Reject\nwith full audit trail"]
        COP["Co-Pilot\nask Claude anything"]
    end

    CON --> DEB
    ACT --> APP
    Graph --> COP

    style Signals fill:#1e293b,stroke:#334155,color:#e2e8f0
    style Agents fill:#172554,stroke:#1e40af,color:#bfdbfe
    style Graph fill:#1c1917,stroke:#78716c,color:#e7e5e4
    style Human fill:#422006,stroke:#b45309,color:#fef3c7
```

---

## Three Views, One System

### 1. Command Dashboard
The main operational view. Six panels show the full picture at a glance:

- **Signal Intelligence** — Claude's real-time analysis of each incoming signal (images, audio, text) with per-source confidence scores
- **Situation Map** — Leaflet map with live incident markers, resource positions, and sector overlays
- **Decision Queue** — Contradictions and action recommendations ranked by urgency, with explicit tradeoffs
- **Evidence Flow** — ReactFlow graph showing how signals connect to incidents, contradictions, and decisions
- **Resource Status** — Ambulances, fire trucks, SAR teams, helicopters — all trackable
- **Event Timeline** — Chronological audit trail of every event and decision

### 2. Debate Room
When two sources contradict each other, click **"Watch Agents Debate"** to open a live, multi-turn argument between 4 Claude agents:

| Role | What it does |
|------|-------------|
| **Defender** | Argues for Claim A with evidence and reasoning |
| **Challenger** | Argues for Claim B, poking holes in Claim A |
| **Rebuttal** | Responds to the Challenger, integrating new evidence |
| **Synthesis** | Weighs both sides and produces a final confidence-scored verdict |

Each turn streams to the UI in real time. After the synthesis, the operator can **Accept Claim A**, **Accept Claim B**, or **Request Aerial Verification**.

### 3. Operator Co-Pilot
A conversational Claude interface with full access to the situation graph. Ask questions like:

- *"What's the highest-risk area right now?"*
- *"Should I reroute ambulances from Sector 1?"*
- *"What's our hospital capacity situation?"*

Claude answers with specific incident IDs, confidence levels, and resource references — not generic advice.

---

## The Six Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **VisionAgent** | Damage assessment, casualty estimation | Drone/satellite imagery | Damage level, trapped indicators, access routes |
| **AudioAgent** | Transcript analysis, urgency classification | 911 calls, radio dispatches | Incident type, persons involved, resource requests |
| **TextAgent** | Credibility scoring, claim extraction | Reports, social media | Claims with confidence, source credibility |
| **VerificationAgent** | Cross-source contradiction detection | Multiple claims about same entity | Verdict (contradiction/consistent), temporal analysis |
| **PlanningAgent** | Resource allocation with explicit tradeoffs | Full situation graph | Recommendations with tradeoffs and uncertainty factors |
| **TemporalAgent** | Confidence decay, situation projection | Time-series observations | Projected state, staleness flags, refresh priorities |

Every agent has a **fallback mode** with realistic pre-built scenarios so the demo works even without an API key.

---

## Demo Scenario: Metro City 6.8 Earthquake

The simulation plays out 15 events in ~30 seconds:

| Time | Event | What Happens |
|------|-------|-------------|
| T+5s | Drone image | Severe pancake collapse at 500 Market Street |
| T+8s | Social media | Panicked tweets confirm the collapse |
| T+12s | Radio dispatch | First responder reports 5+ trapped, requests SAR |
| T+15s | Drone image | Active fire spreading in Sector 3 |
| T+18s | Hospital report | Metro General at 45% ER capacity |
| T+22s | 911 call | Family of 4 trapped on 3rd floor, Oak Street |
| T+32s | **Contradiction** | Bridge: satellite says intact, radio says collapsed |
| T+38s | **Contradiction** | Casualties: field says 12-15, hospital says only 3 received |
| T+46s | **Contradiction** | Gas line: sensors say nominal, civilian reports gas smell |
| T+55s | Aerial verify | HELI-1 confirms bridge collapse |
| T+68s | 911 transcript | Second report of trapped family, corroborates first |
| T+120s | **Aftershock 4.2M** | Confidence levels decay across all incidents |
| T+125s | Ground camera | Secondary collapse in Sector 3 |
| T+130s | Utility alert | Gas leak confirmed at Oak/Elm intersection |

### What to Show Judges

1. **Click Play** — watch all 15 events stream in with real-time Claude analysis
2. **Spot the contradictions** — 3 amber cards appear in the Decision Queue
3. **Open the Debate Room** — click "Watch Agents Debate" on any contradiction card, then click "Start Debate" to see 4 Claude agents argue live
4. **Make a decision** — Accept one claim, reject the other, or send aerial verification
5. **Approve the plan** — the Planning Agent recommends resource deployment with explicit tradeoffs
6. **Aftershock hits** — watch confidence levels decay across the board
7. **Ask the Co-Pilot** — switch to the Co-Pilot tab and ask "What's the highest-risk area?"

---

## Architecture

```
backend/
├── main.py                  # FastAPI entry + lifespan
├── config.py                # Pydantic settings
├── agents/
│   ├── base_agent.py        # BaseAgent ABC (async API + fallback)
│   ├── vision_agent.py      # Multimodal image analysis
│   ├── audio_agent.py       # Audio/transcript processing
│   ├── text_agent.py        # Text credibility + claim extraction
│   ├── verification_agent.py # Cross-modal contradiction detection
│   ├── planning_agent.py    # Resource allocation with tradeoffs
│   ├── temporal_agent.py    # Confidence decay + projection
│   └── debate_agent.py      # 4-turn structured debate orchestrator
├── graph/
│   ├── schemas.py           # 25+ Pydantic models
│   └── situation_graph.py   # In-memory graph with audit log
├── orchestrator/
│   ├── coordinator.py       # Main orchestration + signal routing
│   └── simulation.py        # Demo scenario playback engine
├── api/
│   ├── routes.py            # REST endpoints
│   ├── websocket.py         # Real-time broadcast to all clients
│   └── copilot.py           # Conversational Claude endpoint
└── demo_data/
    └── scenario_earthquake.json

frontend/
├── src/
│   ├── App.tsx              # Router + WebSocket handler
│   ├── components/
│   │   ├── layout/          # Dashboard, Header, Panel
│   │   ├── signals/         # SignalIntelligence (per-modality cards)
│   │   ├── decisions/       # DecisionQueue, ContradictionCard, ActionCard
│   │   ├── map/             # MapView (Leaflet)
│   │   ├── evidence/        # EvidenceFlow (ReactFlow)
│   │   ├── resources/       # ResourcePanel + hospital capacity
│   │   ├── timeline/        # EventTimeline
│   │   └── shared/          # ConfidenceBadge, UrgencyBadge, Countdown
│   ├── pages/
│   │   ├── DebatePage.tsx   # Live agent debate room
│   │   └── CopilotPage.tsx  # Conversational co-pilot
│   ├── hooks/
│   │   ├── useSituationGraph.ts  # Zustand store (full app state)
│   │   └── useWebSocket.ts       # Auto-reconnecting WebSocket
│   └── types/
│       ├── index.ts         # Core domain types
│       └── debate.ts        # Debate turn types
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI | Claude Opus 4.6 via Anthropic SDK |
| Backend | Python 3.11, FastAPI, Pydantic v2 |
| Real-time | WebSocket (native FastAPI) |
| Frontend | React 18, TypeScript (strict), Tailwind CSS, Vite |
| Map | Leaflet + react-leaflet |
| Flow visualization | React Flow |
| State management | Zustand |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Anthropic API key

### Setup

```bash
# 1. Add your API key
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# 2. Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** and click the **Play** button.

---

## Key Design Decisions

- **Non-blocking API calls**: All Claude calls use `asyncio.to_thread()` so the event loop stays responsive during long API responses
- **Fire-and-forget simulation**: Signal events dispatch as background tasks — the simulation pacing is independent of API latency
- **Graceful degradation**: Every agent has a `get_fallback_output()` with realistic pre-built data, so the demo works without an API key
- **Optimistic UI updates**: Approve/Reject buttons update locally before the server confirms, so the UI feels instant
- **Per-message error handling**: WebSocket errors in individual message handlers don't disconnect the client

---

## Why Claude?

- **Multimodal reasoning** — damage assessment from image descriptions without fine-tuning
- **Structured JSON output** — reliable extraction with bracket-counting fallback for malformed responses
- **Multi-turn debate** — 4 agents argue across turns with growing context, producing a synthesized verdict
- **Epistemic honesty** — Claude naturally hedges and acknowledges uncertainty, which is exactly what disaster response needs
- **Cross-modal verification** — VerificationAgent compares claims across image, audio, and text sources

---

## License

MIT — see [LICENSE](LICENSE)
