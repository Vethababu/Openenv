import requests
import time
import sys
 
URL = "http://localhost:7860"
 
OPTIMAL_ACTIONS = {
    "code_easy":   ["fix_syntax", "fix_logic", "add_test"],
    "code_medium": ["fix_syntax", "fix_logic", "refactor"],
    "sys_hard":    ["ls", "create_file", "pip_install"],
}
 
 
def run_task(task: str):
    agent_name = f"baseline_{task}"
 
    # Reset
    try:
        r = requests.post(f"{URL}/reset",
                          json={"agent_name": agent_name, "task": task},
                          timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] reset failed: {e}", flush=True)
        return
 
    print(f"[START] task={task}", flush=True)
 
    actions = OPTIMAL_ACTIONS.get(task, ["no_change"]) + ["no_change"] * 10
    total_reward = 0.0
    final_score = 0.0
    step_num = 0
 
    for action in actions:
        try:
            res = requests.post(f"{URL}/step",
                                json={"agent_name": agent_name, "action": action},
                                timeout=10).json()
        except Exception as e:
            print(f"[ERROR] step failed: {e}", flush=True)
            break
 
        reward = res["reward"]
        done = res["done"]
        score = res.get("info", {}).get("score", 0.0)
        if score is None:
            score = 0.0
        total_reward += reward
        step_num += 1
 
        print(f"[STEP] step={step_num} action={action} reward={reward:.4f} done={done} score={score:.4f}", flush=True)
 
        if score:
            final_score = score
