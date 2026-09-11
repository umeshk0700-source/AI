# Day 32 — Packaging & Infrastructure as Code

Turn the Day 30 RAG API into a reproducible container image and describe its infrastructure as
code you can plan, apply, and diff. Docker and Terraform can't run in a notebook, so you build
the mental models from scratch — a layer-cache simulator and a ~60-line declarative resource
engine with plan/apply/drift — and read the real `Dockerfile` / `main.tf` alongside.

## Learning objectives

1. Explain what a container image is (layers, content-addressing) and why layer order controls build speed.
2. Write a production `Dockerfile` for a Python LLM service: multi-stage, non-root, cached deps.
3. Explain the declarative model: desired vs recorded (state) vs real state; plan = the diff.
4. Implement `plan` / `apply` / drift-detection for a small resource graph with dependencies.
5. Read a Terraform config for ECR + Lambda + API Gateway and say what each block does.
6. List what must not go in an image (secrets, config) and how it gets in at runtime.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | "Works on my machine" → artifact + declared infra | 4 min |
| 1 | The bash-script deploy, and watching it drift | 8 min |
| 2 | Container images from scratch: layers & caching | 13 min |
| 3 | A declarative infra engine: plan / apply / drift | 14 min |
| 4 | The real Terraform, block by block | 6 min |
| 5 | Config & secrets: the 12-factor cut that matters | 12 min |
| 6 | Bridge to CI/CD | 3 min |
| 7 | Exercises and self-check quiz | — |

## Setup

```bash
source ../../../.venv/bin/activate
```

Pure standard library. No Docker, Terraform, or cloud account. The notebook writes example
`Dockerfile`, `.dockerignore`, and `main.tf` files into this folder as it runs.

## Run it

```bash
python -m jupyterlab projects/week-11-mlops-and-mcp/day-32-package-and-iac/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Docker — best practices for writing Dockerfiles — https://docs.docker.com/build/building/best-practices/
- The Twelve-Factor App — https://12factor.net
- Terraform — language & workflow — https://developer.hashicorp.com/terraform/language
- OCI Image Spec — https://github.com/opencontainers/image-spec

## Files

- `lesson.ipynb` — the guided lesson.
- `solutions/solutions.ipynb` — worked solutions + answer key.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — none (standard library only).
