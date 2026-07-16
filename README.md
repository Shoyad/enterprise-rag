# enterprise-rag

A **production-minded** knowledge assistant that answers questions from a company's own
internal documents — with citations, and an honest "I don't have enough information"
instead of a guess.

This is a clean-room engineering sample: **no proprietary code, client data, real names,
or credentials**. The demo runs on a generated, fictional enterprise knowledge base.

## Current Status

- ✅ Repository architecture
- 🚧 Backend bootstrap
- ⬜ Document ingestion
- ⬜ Chunking
- ⬜ Embeddings
- ⬜ Retrieval
- ⬜ Answer generation
- ⬜ Streaming
- ⬜ Evaluation
- ⬜ CI/CD

Only ticked items are implemented. Nothing is claimed as working until it is. This is a
**reference implementation in active development**, not a finished product.

---

## The problem

Teams drown in internal documents — handbooks, playbooks, catalogs, security policies.
Staff waste time hunting for answers, and generic LLM chat invents plausible-but-wrong
ones. A trustworthy internal assistant must answer **only** from the company's documents,
**cite** its sources, and **abstain** when the documents don't contain the answer.

## What this project does *not* do

- **It never fabricates answers.** There is no fake or simulated LLM. If no generation
  provider is configured, the API returns a clear configuration error explaining how to
  set up OpenAI or Anthropic — it does not pretend to answer.
- Retrieval runs fully locally (open-source embeddings), so you can ingest and search
  with **zero API keys**; only generated answers require a provider key.

---

## Architecture (at a glance)

Layers are separated so each can be tested and swapped in isolation:
**API · parsing · chunking · embeddings · ingestion · retrieval · generation ·
persistence · background jobs · evaluation.** Diagram, decisions, and trade-offs in
[`docs/architecture.md`](docs/architecture.md).

- **Ingestion** (background worker): upload → parse (PDF/Markdown) → chunk → embed →
  store in PostgreSQL/pgvector. Uploads return immediately.
- **Query**: embed question → vector search → assemble cited context → grounded
  generation → stream the answer over SSE.

---

## Technology decisions (summary)

| Choice | Why |
|---|---|
| **Python 3.12 + FastAPI** | async, typed, SSE-friendly, standard for AI backends |
| **PostgreSQL + pgvector** | documents *and* vectors in one datastore → simpler ops, transactional |
| **Redis + arq** | lightweight async background jobs; ingestion shouldn't block uploads |
| **FastEmbed (local embeddings)** | real open-source model, keyless retrieval, small image |
| **OpenAI / Anthropic (generation)** | real providers, opt-in via key; no fake fallback |
| **uv · SQLAlchemy 2.0 · structlog · pydantic-settings** | fast deps, typed ORM, JSON logs, typed config |

Full rationale — including **why pgvector over Pinecone/Weaviate**, chunking strategy,
hallucination mitigation, and cost/latency — lives in
[`docs/architecture.md`](docs/architecture.md), each decision documented with *Why /
Alternatives / Trade-offs / Limitations*.

---

## Docker strategy

`docker compose` brings up four services: `db` (`pgvector/pgvector:pg16`),
`redis` (`redis:7-alpine`), `api` (this repo, FastAPI), and `worker` (arq). Config is
entirely environment-driven (`.env`, see `.env.example`).

> The compose file and Dockerfile are committed as the deployment strategy; they become
> runnable at the **backend bootstrap** milestone, once the application entrypoint exists.

---

## Local setup *(available from the bootstrap milestone onward)*

```bash
cp .env.example .env
docker compose up --build      # api on :8000, worker, db, redis
make ingest-demo               # generate + ingest the fictional demo knowledge base
make query Q="What is the returns policy?"   # requires a generation provider key
make test
make eval
```

Commands are documented ahead of implementation so the intended UX is reviewable; each
becomes real in its milestone and is verified before that milestone is marked done.

---

## Repository layout

```
src/app/
  api/          HTTP routes
  parsing/      PDF + Markdown → text
  chunking/     token-aware chunker
  embeddings/   provider abstraction (fastembed / openai)
  ingestion/    orchestration + background jobs
  retrieval/    pgvector search + metrics
  generation/   cited, grounded answers (real providers only)
  persistence/  models, repository, db
docs/           architecture + operating guide
demo/           screenshots, diagram, sample requests, short video
eval/           evaluation dataset + runner
scripts/        demo knowledge-base generator
tests/          unit + integration
migrations/     alembic
```

## Demo knowledge base

The demo ingests a **reusable, fully fictional enterprise document set** (generated, not
copied): Employee Handbook, Engineering Playbook, Product Catalog, Support FAQ, Security
Policy, Incident Response Guide, an ADR, Release Notes, and an HR Policy. This shows the
system against a realistic, generic knowledge base rather than one contrived question.

## Limitations (by design, this iteration)

No authentication/multi-tenancy, no reranking, no hybrid keyword search, no web UI, no OCR
for scanned PDFs, single embedding dimension per database. Each is a conscious scope
decision tracked in the roadmap — not an accidental gap.

## License & security

MIT (see [`LICENSE`](LICENSE)). No secrets committed; see [`SECURITY.md`](SECURITY.md).
