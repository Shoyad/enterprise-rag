# Security

## Posture

- **Keyless by default.** The demo runs entirely locally (FastEmbed embeddings + stub
  generation) with no external API keys. Cloud providers are strictly opt-in via `.env`.
- **No secrets in Git.** Only `.env.example` is committed. `.env` is git-ignored.
- **No proprietary or client data.** All demo documents are generated for a fictional
  company. No real names, credentials, schemas, or business data appear in this repo or
  its history.

## Reporting a vulnerability

This is a portfolio reference implementation. If you spot a security issue, please open a
GitHub issue (omit any sensitive details) or contact the maintainer via the profile page.

## Notes for reviewers

- Uploaded files are parsed, not executed.
- Generation is constrained to retrieved context; there is no tool execution or shell
  access in the answer path.
