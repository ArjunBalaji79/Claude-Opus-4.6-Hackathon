# CrisisCore - Claude Code Instructions

## What We're Building

**CrisisCore** is a multimodal, multi-agent disaster response coordination system for the Anthropic Hackathon.

**One-liner:** Transform chaotic disaster signals (images, audio, text) into prioritized, auditable response decisions with visible uncertainty.

**Key insight:** Most disaster AI hides uncertainty. We surface it. When agents disagree, humans see why.

## Project Structure

```
crisiscore/
├── backend/
│   ├── main.py              # FastAPI entry
│   ├── config.py            # Settings + API keys
│   ├── agents/              # All AI agents
│   ├── graph/               # Situation graph
│   ├── orchestrator/        # Coordination logic
│   ├── api/                 # REST + WebSocket
│   └── demo_data/           # Scenario files
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   └── types/           # TypeScript types
│   └── public/
└── scripts/
```

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Anthropic SDK
- **Frontend:** React 18, TypeScript, Tailwind, Vite
- **Map:** Leaflet + React-Leaflet
- **Flow Viz:** React Flow
- **AI:** Claude Opus 4.6 (`claude-opus-4-5-20251101`)

## Current Phase

Check `docs/PROGRESS.md` for current status.

## Key Commands

```bash
# Backend
cd backend && uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm run dev

# Run demo
python scripts/run_demo.py
```

## Important Files to Reference

| When working on... | Read this first |
|-------------------|-----------------|
| Any agent | `docs/AGENTS.md` |
| Backend API | `docs/API.md` |
| Frontend components | `docs/FRONTEND.md` |
| Demo scenario | `docs/DEMO_SCENARIO.md` |
| Data schemas | `docs/SCHEMAS.md` |

## Code Style

- Python: Type hints everywhere, Pydantic for models
- TypeScript: Strict mode, interfaces over types
- Components: Functional with hooks, no classes
- Naming: `snake_case` Python, `camelCase` TypeScript

## Agent Architecture Pattern

Every agent follows this pattern:
```python
class SomeAgent(BaseAgent):
    def get_system_prompt(self) -> str: ...
    def format_input(self, raw_input) -> list[dict]: ...
    def parse_output(self, response: str) -> AgentOutput: ...
```

See `docs/AGENTS.md` for full specs.

## The "Win" Criteria

1. **Most Creative:** Cross-modal contradiction detection, agents that argue
2. **Keep Thinking:** Epistemic transparency, explicit tradeoffs
3. **Demo Impact:** Chaos → contradiction → resolution → evolution arc
