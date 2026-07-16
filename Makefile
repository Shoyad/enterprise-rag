# Developer entrypoints. Targets marked [M#] become functional at that milestone.
.PHONY: up down fmt lint type test eval ingest-demo query

up:            ## start all services            [M2]
	docker compose up --build

down:
	docker compose down -v

fmt:
	uv run ruff format . && uv run ruff check --fix .

lint:
	uv run ruff check .

type:
	uv run mypy src

test:          ## unit + integration            [M7]
	uv run pytest

eval:          ## retrieval + citation metrics   [M7]
	uv run python eval/run_eval.py

ingest-demo:   ## generate + ingest demo docs    [M4]
	uv run python scripts/generate_demo_docs.py

query:         ## query the assistant            [M6]
	@echo "usage: make query Q=\"your question\"  (available at M6)"
