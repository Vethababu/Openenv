[README.md](https://github.com/user-attachments/files/26655423/README.md)
# Real-World OpenEnv

A complete [OpenEnv](https://openenv.dev)-compatible environment for training AI agents on real-world software engineering tasks: code debugging and system operations.

---

## Tasks

| Task | Difficulty | Max Steps | Reward |
|---|---|---|---|
| `code_easy` | Easy | 15 | 0.0 → 1.0 (tests passed) |
| `code_medium` | Medium | 20 | 0.0 → 1.0 (tests + efficiency) |
| `sys_hard` | Hard | 25 | 0.0 → 1.0 (goal progress) |

### `code_easy`
Fix a simple Python function with a syntax error, then a logic bug, then add a passing test.

### `code_medium`
Fix an off-by-one recursion bug across multiple stages. Efficiency bonus for fewer steps.

### `sys_hard`
Simulate a terminal session: inspect a virtual filesystem, create a file, and install a dependency.

---

## Observation Space

**code_easy / code_medium:**
```json
{
  "code_snippet": "def add(a, b):\n    return a",
  "error": "SyntaxError: unexpected EOF",
  "tests_passed": 0,
  "max_tests": 3,
  "stage": 0,
  "steps_remaining": 15
}
```

**sys_hard:**
```json
{
  "cur_dir": "/app",
  "files": "requirements.txt:fastapi\nuvicorn",
  "task_goal": "numpy installed: numpy.py exists with 'import numpy' and numpy in requirements.txt",
  "progress": 0.0,
  "steps_remaining": 25
}
```

---

## Action Space

| Task | Actions |
|---|---|
| `code_easy` | `no_change`, `fix_syntax`, `fix_logic`, `add_test` |
| `code_medium` | `no_change`, `fix_syntax`, `fix_logic`, `refactor` |
| `sys_hard` | `ls`, `pip_install`, `create_file`, `cd` |

---

## API

| Endpoint | Method | Body | Description |
|---|---|---|---|
| `/reset` | POST | `{agent_name, task}` | Start/restart session |
| `/step` | POST | `{agent_name, action}` | Take one step |
| `/state` | POST | `{agent_name}` | Get current observation |

---

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860 --reload

# In another terminal:
python inference.py
```

## Run Tests (no server needed)

```bash
python test_env.py
```

## Docker

```bash
docker build -t real-world-openenv .
docker run -p 7860:7860 real-world-openenv

# Then run inference:
python inference.py
```

---

## Baseline Scores (deterministic agent)

| Task | Score | Steps |
|---|---|---|
| `code_easy` | 1.0000 | 3 |
| `code_medium` | ~0.9900 | 3 |
| `sys_hard` | 1.0000 | 3 |

---

## Project Structure

```
├── app.py          # FastAPI server
├── env.py          # Environment classes + registry
├── tasks.py        # Task configs (buggy code, goals)
├── grader.py       # Reward/score functions
├── models.py       # Pydantic models
├── inference.py    # Baseline agent script
├── test_env.py     # Standalone env tests
├── openenv.yaml    # OpenEnv spec
├── Dockerfile      # Container definition
└── requirements.txt
```
