import uvicorn
from fastapi import FastAPI
from typing import Dict, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import OpenEnvRegistry
from models import ConfigRequest, AgentRequest, StepRequest

app = FastAPI(
    title="Real-World OpenEnv",
    description="OpenEnv API for AI agent training",
    version="2.0",
)

sessions: Dict[str, Any] = {}

@app.get("/")
def root():
    return {
        "name": "Real-World OpenEnv",
        "version": "2.0",
        "tasks": ["code_easy", "code_medium", "sys_hard"],
        "endpoints": ["/reset", "/step", "/state"],
    }

@app.post("/reset")
def reset(req: Optional[ConfigRequest] = None):
    if req is None:
        req = ConfigRequest()
    env_instance = OpenEnvRegistry.create(req.task)
    obs = env_instance.reset({"task": req.task})
    sessions[req.agent_name] = env_instance
    return {"observation": obs["observation"]}

@app.post("/step")
def step(req: Optional[StepRequest] = None):
    if req is None:
        req = StepRequest()
    if req.agent_name not in sessions:
        env_instance = OpenEnvRegistry.create("code_easy")
        env_instance.reset({"task": "code_easy"})
        sessions[req.agent_name] = env_instance
    result = sessions[req.agent_name].step(req.action)
    return {
        "observation": result["observation"],
        "reward": result["reward"],
        "done": result["done"],
        "info": result.get("info", {}),
    }

@app.post("/state")
def state(req: Optional[AgentRequest] = None):
    if req is None:
        req = AgentRequest()
    if req.agent_name not in sessions:
        env_instance = OpenEnvRegistry.create("code_easy")
        env_instance.reset({"task": "code_easy"})
        sessions[req.agent_name] = env_instance
    obs = sessions[req.agent_name].state()
    return {"observation": obs["observation"]}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
