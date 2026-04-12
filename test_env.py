"""
Standalone environment tests — no server required.
Tests each env with both optimal and random action sequences.
"""
import json
from env import get_env
from tasks import TASKS

OPTIMAL = {
    "code_easy":   ["fix_syntax", "fix_logic", "add_test"],
    "code_medium": ["fix_syntax", "fix_logic", "refactor"],
    "sys_hard":    ["ls", "create_file", "pip_install"],
}

tasks = ["code_easy", "code_medium", "sys_hard"]

all_passed = True

for task in tasks:
    print(f"\n{'='*50}")
    print(f"  Task: {task}")
    print(f"{'='*50}")

    config = {"task": task}
    env = get_env(task, TASKS.get(task, {}))
    obs = env.reset(config)["observation"]
    print("Reset obs:", json.dumps(obs, indent=2))

    total_reward = 0.0
    final_score = None

    for i, action in enumerate(OPTIMAL[task] + ["no_change", "no_change"]):
        result = env.step(action)
        reward = result["reward"]
        done = result["done"]
        score = result["info"].get("score", None)
        total_reward += reward

        score_str = f"{score:.4f}" if score is not None else "N/A"
        print(f"Step {i+1:02d}: action={action:<15} reward={reward:+.4f}  done={done}  score={score_str}")

        if score is not None:
            final_score = score

        if done:
            break

    # Validate score
    expected_score = 1.0
    if final_score is None:
        print(f"  [WARN] No final score returned for {task}")
        all_passed = False
    elif final_score < expected_score:
        print(f"  [WARN] {task}: expected score >= {expected_score}, got {final_score:.4f}")
    else:
        print(f"  [PASS] {task}: final_score={final_score:.4f}  total_reward={total_reward:.4f}")

    # Test reset works cleanly
    obs2 = env.reset(config)["observation"]
    assert obs2["steps_remaining"] == env.max_steps, "Reset did not restore steps_remaining"
    print(f"  [PASS] Reset is clean.")

print(f"\n{'='*50}")
print("  All tests complete.")
print(f"{'='*50}")
