import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 
from env import OpenEnvRegistry
from openai import OpenAI
import time
 
# Use the injected proxy credentials
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY", "placeholder")
 
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)
 
SYSTEM_PROMPT = """You are an AI agent solving environment tasks.
You will be given the current observation and must choose the best action.
Reply with ONLY the action string, nothing else.
"""
 
ACTION_SPACES = {
    "code_easy":   ["no_change", "fix_syntax", "fix_logic", "add_test"],
    "code_medium": ["no_change", "fix_syntax", "fix_logic", "refactor"],
    "sys_hard":    ["ls", "pip_install", "create_file", "cd"],
}
 
 
def get_action(task: str, observation: dict) -> str:
    action_space = ACTION_SPACES.get(task, ["no_change"])
    prompt = f"""Task: {task}
Current observation: {json.dumps(observation, indent=2)}
Available actions: {action_space}
Choose the best action from the list above. Reply with ONLY the action string."""
 
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=20,
            temperature=0.0,
        )
        action = response.choices[0].message.content.strip().lower()
        # Make sure it's a valid action
        if action not in action_space:
            action = action_space[0]
        return action
    except Exception as e:
        print(f"[WARN] LLM call failed: {e}, using default action", flush=True)
        return action_space[0]
 
 
def run_task(task: str):
    env = OpenEnvRegistry.create(task)
    result = env.reset({"task": task})
    obs = result["observation"]
 
    print(f"[START] task={task}", flush=True)
 
    total_reward = 0.0
    final_score = 0.0
    step_num = 0
    max_steps = 15
 
    while step_num < max_steps:
        action = get_action(task, obs)
        result = env.step(action)
 
        obs = result["observation"]
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
        time.sleep(0.2)
 
