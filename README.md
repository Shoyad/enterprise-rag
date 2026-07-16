# enterprise-rag

An **engineering-focused reference implementation** of a Retrieval-Augmented Generation
(RAG) assistant over internal company documents.

RAG-over-your-documents is a commodity; the engineering around it is not. This repository
is built to show *how* such a system is engineered — not merely that another one exists:

- **Evaluation before optimization** — retrieval/answer quality is measured with a harness, not asserted.
- **Citation correctness** — every answer traces to source chunks, and citations are validated against what was retrieved.
- **Abstention over hallucination** — "I don't have enough information" when the documents don't contain the answer.
- **Production-minded architecture** — separated, testable layers; ingestion runs in the background.
- **Operational reliability** — health checks, structured logs, idempotent jobs, an audit trail.
- **Honest trade-off documentation** — each decision states Why / Alternatives / Trade-offs / Limitations.
- **No fake AI** — generated answers require a real provider; unconfigured, the API returns an error, it never simulates.

Clean-room sample: **no proprietary code, client data, real names, or credentials**. It runs
on a generated, fictional enterprise knowledge base.

## Current Status

- ✅ Repository architecture
- ✅ Backend bootstrap
- 🚧 Document ingestion
- ⬜ Chunking
- ⬜ Embeddings
- ⬜ Retrieval
- ⬜ Answer generation
- ⬜ Streaming
- ⬜ Evaluation
- ⬜ CI/CD

Only ticked items are implemented. This is a **reference implementation in active
development**, not a finished product.

---

## The problem

Teams drown in internal documents — handbooks, playbooks, catalogs, security policies.
Staff waste time hunting for answers, and generic LLM chat invents plausible-but-wrong
ones. A trustworthy internal assistant must answer **only** from the company's documents,
**cite** its sources, and **abstain** when the documents don't contain the answer.

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
| **FastEmbed (local embeddings)** | one real open-source model, keyless retrieval, small image; a minimal interface leaves room for another provider *if ever needed* |
| **OpenAI / Anthropic (generation)** | real providers, opt-in via key; no fake fallback |
| **uv · SQLAlchemy 2.0 · structlog · pydantic-settings** | fast deps, typed ORM, JSON logs, typed config |

Full rationale — **why pgvector over Pinecone/Weaviate**, chunking strategy, hallucination
mitigation, cost/latency — lives in [`docs/architecture.md`](docs/architecture.md), each
decision documented as *Why / Alternatives / Trade-offs / Limitations*.

---

## Docker strategy

`docker compose` brings up four services: `db` (`pgvector/pgvector:pg16`),
`redis` (`redis:7-alpine`), `api` (this repo, FastAPI), and `worker` (arq). Config is
entirely environment-driven (`.env`, see `.env.example`).

---

## Local setup

```bash
cp .env.example .env
docker compose up --build      # api on :8000, worker, db, redis
curl localhost:8000/health     # available now
# the commands below become real in their milestones:
make ingest-demo               # generate + ingest the fictional demo knowledge base
make query Q="What is the returns policy?"   # requires a generation provider key
make test
make eval
```

---

## Repository layout

```
src/app/
  api/          HTTP routes
  parsing/      PDF + Markdown → text
  chunking/     token-aware chunker
  embeddings/   local FastEmbed behind a minimal interface
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
Policy, Incident Response Guide, an ADR, Release Notes, and an HR Policy — a realistic,
generic knowledge base rather than one contrived question.

## Limitations (by design, this iteration)

No authentication/multi-tenancy, no reranking, no hybrid keyword search, no web UI, no OCR
for scanned PDFs. Each is a conscious scope decision tracked in the roadmap — not an
accidental gap.

## License & security

MIT (see [`LICENSE`](LICENSE)). No secrets committed; see [`SECURITY.md`](SECURITY.md).
