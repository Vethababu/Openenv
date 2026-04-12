import os
import uvicorn
from fastapi import FastAPI, HTTPException
from env import OpenEnvRegistry
from models import ConfigRequest, AgentRequest, StepRequest, ObservationResponse, StepResponse
from typing import Dict, Any
 
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
 
 
@app.post("/reset", response_model=ObservationResponse)
def reset(req: ConfigRequest):
    env_instance = OpenEnvRegistry.create(req.task)
    obs = env_instance.reset({"task": req.task})
    sessions[req.agent_name] = env_instance
    return ObservationResponse(observation=obs["observation"])
 
 
@app.post("/step", response_model=StepResponse)
def step(req: StepRequest):
    if req.agent_name not in sessions:
        raise HTTPException(status_code=400, detail=f"No session for agent '{req.agent_name}'. Call /reset first.")
    result = sessions[req.agent_name].step(req.action)
    return StepResponse(
        observation=result["observation"],
        reward=result["reward"],
        done=result["done"],
        info=result.get("info", {}),
    )
 
 
@app.post("/state", response_model=ObservationResponse)
def state(req: AgentRequest):
    if req.agent_name not in sessions:
        raise HTTPException(status_code=400, detail=f"No session for agent '{req.agent_name}'. Call /reset first.")
    obs = sessions[req.agent_name].state()
    return ObservationResponse(observation=obs["observation"])
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
 
