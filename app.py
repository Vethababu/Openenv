import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from env import OpenEnvRegistry
from models import ConfigRequest, AgentRequest, StepRequest, ObservationResponse, StepResponse
from typing import Dict, Any, Optional
 
app = FastAPI(
    title="Real-World OpenEnv",
    description="OpenEnv API for AI agent training: code debugging & system ops tasks.",
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
    """
    Reset the environment. Body is optional — defaults to agent_name=default_agent, task=code_easy.
    """
    if req is None:
        req = ConfigRequest()
    env_instance = OpenEnvRegistry.create(req.task)
    obs = env_instance.reset({"task": req.task})
    sessions[req.agent_name] = env_instance
    return {"observation": obs["observation"]}
 
 
@app.post("/step")
def step(req: Optional[StepRequest] = None):
    """
    Take one action. Body is optional — defaults to agent_name=default_agent, action=no_change.
    """
    if req is None:
        req = StepRequest()
    if req.agent_name not in sessions:
        # Auto-reset with default task if no session exists
        env_instance = OpenEnvRegistry.create("code_easy")
        obs = env_instance.reset({"task": "code_easy"})
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
    """
    Get current observation without stepping.
    """
    if req is None:
        req = AgentRequest()
    if req.agent_name not in sessions:
        env_instance = OpenEnvRegistry.create("code_easy")
        obs = env_instance.reset({"task": "code_easy"})
        sessions[req.agent_name] = env_instance
    obs = sessions[req.agent_name].state()
    return {"observation": obs["observation"]}
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
