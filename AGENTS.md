# AGENTS.md

## Project Name
School Informatization MVP

## Project Goal
Build an MVP for school informatization. The system should help a school manage its core digital workflow step by step.

## Important Documents
Before making changes, always read these documents:

1. `docs/01-mvp-scope.md`
2. `docs/02-user-journey.md`
3. `docs/03-entities-relationships.md`
4. `docs/04-api-plan.md` if it exists
5. `docs/05-build-plan.md` if it exists

## Working Style
- Work step by step.
- Do not build everything at once.
- Before coding, explain the small task you will do.
- After coding, summarize what changed.
- Keep the MVP simple.
- Do not add advanced features unless they are already in the docs or explicitly requested.
- Prefer clear and readable code over complicated architecture.

## Tech Stack
Backend: Django + Django REST Framework.
Database: SQLite for MVP.
Authentication: JWT if needed.
Frontend: To be decided later.

## Current MVP Documents
The source of truth is inside the `docs/` folder.
If there is a conflict between chat instructions and code, ask for clarification or follow the latest document.

## Development Rules
- Keep apps/modules organized by domain.
- Add comments only when useful.
- Do not delete existing work without explaining why.
- Do not rename major files without a reason.
- Run tests or basic checks after important changes when possible.

## Git Rules
- Make small changes.
- Use clear commit messages.
- Suggested commit format:
  - `docs: add MVP scope`
  - `backend: create users app`
  - `backend: add school models`
  - `api: add authentication endpoints`