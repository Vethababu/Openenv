import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 
from env import OpenEnvRegistry
from tasks import TASKS
import time
 
OPTIMAL_ACTIONS = {
    "code_easy":   ["fix_syntax", "fix_logic", "add_test"],
    "code_medium": ["fix_syntax", "fix_logic", "refactor"],
    "sys_hard":    ["ls", "create_file", "pip_install"],
}
 
def run_task(task: str):
    env = OpenEnvRegistry.create(task)
    env.reset({"task": task})
 
    print(f"[START] task={task}", flush=True)
 
    actions = OPTIMAL_ACTIONS.get(task, ["no_change"]) + ["no_change"] * 10
    total_reward = 0.0
    final_score = 0.0
    step_num = 0
 
    for action in actions:
        result = env.step(action)
        reward = result["reward"]
        done = result["done"]
        score = result.get("info", {}).get("score", 0.0) or 0.0
        total_reward += reward
        step_num += 1
 
        print(f"[STEP] step={step_num} action={action} reward={reward:.4f} done={done} score={score:.4f}", flush=True)
 
        if score:
            final_score = score
 
        if done:
            break
 
    print(f"[END] task={task} score={final_score:.4f} steps={step_num}", flush=True)
 
 
if __name__ == "__main__":
    for task in ["code_easy", "code_medium", "sys_hard"]:
        run_task(task)
        time.sleep(0.1)
 
