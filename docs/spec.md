#%% Gemini
You are a senior full-stack engineer and AI pair-programmer.
Create a complete MVP for the “ドラフト土地抽選アプリ” (land-draft app) in **one ReAct session**,
following the requirements below. Work in Vibe-Coding style: ①Plan → ②Code → ③Run → ④Refine,
looping automatically until tests pass. Use the directory layout, technology stack,
and algorithm rules provided.

==================== REQUIREMENTS ====================

### 0. Tech stack
- Backend: **FastAPI** + **SQLAlchemy** (Python 3.11)
- DB: **PostgreSQL**
- Frontend: **Next.js 14 (React 18, TypeScript)**, tailwindcss
- Tests: **pytest** and **Playwright**
- Container: **Docker + docker-compose**

### 1. Directory structure (create exactly)
land-draft-app/
 ├ .gemini/config.json            (already exists)
 ├ backend/app/
 │   ├ main.py                    (FastAPI entry)
 │   ├ models.py                  (Land, Voter)
 │   ├ schemas.py                 (Pydantic DTOs)
 │   ├ services/draft.py          (抽選ロジック)
 │   └ tests/                     (unit & integration)
 ├ frontend/src/…                 (Next.js pages & components)
 ├ docs/spec.md                   (project spec; generate from this prompt)
 └ docker-compose.yaml

### 2. Draft algorithm (services/draft.py)
1. **Round 1 (choice1)**
   - Group voters by choice1.
   - If unique → assign immediately.
   - If duplicated → random.choice winner, losers go to next round.
2. **Round 2 (choice2)**
   - Skip voters who already got land in Round 1.
   - ALSO skip voters whose choice2 land was already awarded in Round 1; send them straight to Round 3.
   - Otherwise same grouping/lottery logic.
3. **Round 3 (choice3)**
   - Skip voters who already got land in Round 1 or 2.
   - ALSO skip voters whose choice3 land was awarded in Round 2; send them to Round 4.
   - Same lottery logic.
4. **Round 4 (left-over random)**
   - Randomly shuffle remaining lands and assign to any still-unassigned voters.

### 3. Additional rules
- Max voters ≤ 32, validate input (range 1-32 & no duplicate choices per voter).
- Publish **results per round**, not all at once. Provide `/draft/run?round=N` endpoint or WebSocket event.
- Seed parameter for reproducible lotteries in tests.
- Basic auth (email + OTP) to restrict one vote per person.

### 4. Tasks for this session
1. **PLAN**: output a numbered task list covering scaffolding, models, API routes, algorithm, tests, Docker, and Playwright E2E.
2. **CODE**: generate or modify files step-by-step per plan, committing with `git add` & `git commit -m "..."`.
3. **RUN**: execute `pytest -q` and (when frontend ready) `playwright test` in docker-compose env; fix failures until green.
4. **REFINE**: run `ruff`/`black` lint, improve type hints and docstrings.
5. **DONE**: finish when all tests pass and `docker compose up` starts the stack successfully.

### 5. Constraints
- Use English identifiers in code; comments/docstrings may be bilingual (JP+EN).
- Strictly follow PEP 8 and Google-style docstrings.
- No external dependencies beyond listed stack.
- Keep temperature = 0.2 for deterministic output.

==================== END ====================

When ready, begin with the **PLAN** phase and continue automatically.
Respond only with code blocks or shell commands you intend to run—avoid extra explanations unless an error occurs.