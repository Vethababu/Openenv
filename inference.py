"""
Baseline inference script — runs a rule-based agent on all tasks.
Produces reproducible scores (same action order, no randomness).
Usage:
    # With server running:
    python inference.py
    # To save output:
    python inference.py | tee inf_out.txt
"""

import requests
import time
import sys

URL = "http://localhost:7860"

# Optimal action sequences for each task (deterministic baseline)
OPTIMAL_ACTIONS = {
    "code_easy":   ["fix_syntax", "fix_logic", "add_test"],
    "code_medium": ["fix_syntax", "fix_logic", "refactor"],
    "sys_hard":    ["ls", "create_file", "pip_install"],
}

# Pad with no-ops so we always exhaust a few extra steps
NOOP = {
    "code_easy":   "no_change",
    "code_medium": "no_change",
    "sys_hard":    "ls",
}

MAX_STEPS = 30  # safety cap


def check_server():
    try:
        r = requests.get(URL, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def run_task(task: str) -> dict:
    agent_name = f"baseline_{task}"

    # --- Reset ---
    try:
        r = requests.post(f"{URL}/reset", json={"agent_name": agent_name, "task": task}, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"  [ERROR] /reset failed: {e}")
        return {"task": task, "total_reward": 0.0, "steps": 0, "final_score": 0.0, "error": str(e)}

    obs = r.json()["observation"]
    print(f"  Initial obs: {obs}")

    actions = OPTIMAL_ACTIONS.get(task, []) + [NOOP.get(task, "no_change")] * 10
    total_reward = 0.0
    final_score = 0.0
    steps = 0

    for action in actions:
        if steps >= MAX_STEPS:
            break
        try:
            res = requests.post(
                f"{URL}/step",
                json={"agent_name": agent_name, "action": action},
                timeout=10,
            ).json()
        except Exception as e:
            print(f"  [ERROR] /step failed: {e}")
            break

        reward = res["reward"]
        done = res["done"]
        score = res.get("info", {}).get("score", None)
        total_reward += reward
        steps += 1

        score_str = f"{score:.4f}" if score is not None else "N/A"
        print(f"  Step {steps:02d}: action={action:<15} reward={reward:+.4f}  done={done}  score={score_str}")

        if score is not None:
            final_score = score

        if done:
            break

        time.sleep(0.05)

    return {
        "task": task,
        "total_reward": round(total_reward, 4),
        "steps": steps,
        "final_score": round(final_score, 4),
    }


def main():
    print("=" * 60)
    print("  Real-World OpenEnv — Baseline Inference")
    print("=" * 60)

    if not check_server():
        print(f"\n[ERROR] Server not reachable at {URL}")
        print("Start it with:  uvicorn app:app --host 0.0.0.0 --port 7860")
        sys.exit(1)

    results = []
    for task in ["code_easy", "code_medium", "sys_hard"]:
        print(f"\n=== Task: {task} ===")
        result = run_task(task)
        results.append(result)
        print(f"  >> Total reward: {result['total_reward']:.4f} | Steps: {result['steps']} | Final score: {result['final_score']:.4f}")
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    for r in results:
        status = "PASS" if r["final_score"] >= 1.0 else ("PARTIAL" if r["final_score"] > 0 else "FAIL")
        print(f"  {r['task']:<15} score={r['final_score']:.4f}  reward={r['total_reward']:.4f}  [{status}]")
    avg = sum(r["final_score"] for r in results) / len(results)
    print(f"\n  Average score: {avg:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
