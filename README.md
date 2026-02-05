# Clink AI Backend

> AI-powered loyalty and offer generation engine for retail businesses

A FastAPI microservice that leverages LLMs to analyze customer behavior, generate personalized offers, and create marketing assets. Built with Pydantic AI for structured outputs and designed as a modular AI backend for multi-tenant loyalty programs.

## Features

- **Customer & Order Analysis** — Processes transaction data to extract behavioral insights, cohort patterns, and KPIs
- **AI Offer Generation** — Template-driven offer creation with structured outputs (discounts, winback campaigns, stamp cards, combo offers)
- **Forecast Engine** — Predicts offer performance, redemption rates, and ROI
- **Conversational Chat** — Context-aware AI chat with access to analysis data
- **Coupon Image Generation** — Creates branded marketing materials using multi-pass image generation
- **Multi-tenant Architecture** — Isolated by loyalty program with Redis token auth

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI (async) |
| AI | Pydantic AI (OpenAI, Google, Perplexity) |
| Database | PostgreSQL via asyncpg |
| Cache | Redis |
| Storage | AWS S3 |
| Observability | Logfire |
| Runtime | Python 3.12+ |

## Project Structure

```
backend/app/
├── agents/           # AI agent factory, registry, and prompts
├── analysis/         # Customer & order analysis pipelines
├── api/v2/           # FastAPI routers
├── core/             # Config, settings, model providers
├── crud/             # Database operations
├── schemas/          # Pydantic models & templates
├── services/         # Business logic orchestration
├── summarization/    # KPI summarization for LLM context
└── utils/            # Preprocessing, transformers
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- AWS credentials (for S3)

### Installation

```bash
# Clone the repo
git clone https://github.com/Rikhil-Nell/clink-ai-backend.git
cd clink-ai-backend

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables

```env
# Database
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=5432
DATABASE_NAME=

# Redis
REDIS_URL=redis://localhost:6379

# AI Providers
OPENAI_API_KEY=
GOOGLE_API_KEY=
PERPLEXITY_API_KEY=

# AWS
AWS_ACCESS_KEY=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET=

# Observability
LOGFIRE_TOKEN=
LOGFIRE_ENVIRONMENT=development
```

### Run Development Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Docker

```bash
docker build -t clink-ai-backend .
docker run -p 8000:8000 --env-file .env clink-ai-backend
```

## API Overview

All endpoints require `Authorization` header with a valid token.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/analysis/trigger` | POST | Run customer & order analysis |
| `/api/v2/offer/generate-all-templates` | POST | Generate offers for all templates |
| `/api/v2/offer/update-template` | POST | Regenerate specific template |
| `/api/v2/offer/generate-forecast` | POST | Generate performance forecast |
| `/api/v2/coupon-images/generate` | POST | Create branded coupon image |

## Template System

Offers are generated using a registry of templates:

| Template | Use Case |
|----------|----------|
| `BASIC_DISCOUNT_COUPON` | Standard percentage/flat discounts |
| `WINBACK_MISS_YOU` | Re-engage lapsed customers |
| `VISIT_MILESTONE_FIRST_VISIT` | New customer welcome offers |
| `VISIT_MILESTONE_VISIT_BASED` | Loyalty tiers based on visits |
| `STAMP_CARD_LOYALTY` | Buy X get Y free programs |
| `HAPPY_HOURS_TIME_BASED` | Time-restricted promotions |
| `COMBO_OFFER_STANDARD` | Bundle deals |

Each template has a corresponding Pydantic schema for structured AI outputs.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI    │────▶│   Redis     │
└─────────────┘     │   (Auth)     │     │   (Tokens)  │
                    └──────┬───────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Analysis │ │  Offer   │ │  Image   │
        │ Service  │ │ Service  │ │ Service  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────────────────────────────┐
        │         Agent Factory            │
        │   (Pydantic AI + Prompt Mgmt)    │
        └──────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
     ┌────────┐   ┌────────┐   ┌────────┐
     │ OpenAI │   │ Google │   │Perplxy │
     └────────┘   └────────┘   └────────┘
```

## Development

```bash
# Format code
ruff format .

# Lint
ruff check .

# Type check
pyright
```

## License

AGPL-3.0 — See [LICENSE](LICENSE) for details.
