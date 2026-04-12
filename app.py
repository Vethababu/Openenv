from fastapi import FastAPI, HTTPException
from env import OpenEnvRegistry
from models import ConfigRequest, AgentRequest, StepRequest, ObservationResponse, StepResponse
from typing import Dict, Any

app = FastAPI(
    title="Real-World OpenEnv",
    description="OpenEnv API for AI agent training: code debugging & system ops tasks.",
    version="2.0",
)

# agent_name -> env instance
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
    """
    Start or restart a session for agent_name on the given task.
    Returns the initial observation.
    """
    env_instance = OpenEnvRegistry.create(req.task)
    obs = env_instance.reset({"task": req.task})
    sessions[req.agent_name] = env_instance
    return ObservationResponse(observation=obs["observation"])


@app.post("/step", response_model=StepResponse)
def step(req: StepRequest):
    """
    Take one action in the environment.
    Call /reset first to initialise a session.
    """
    if req.agent_name not in sessions:
        raise HTTPException(
            status_code=400,
            detail=f"No session for agent '{req.agent_name}'. Call /reset first.",
        )
    env_instance = sessions[req.agent_name]
    result = env_instance.step(req.action)
    return StepResponse(
        observation=result["observation"],
        reward=result["reward"],
        done=result["done"],
        info=result.get("info", {}),
    )


@app.post("/state", response_model=ObservationResponse)
def state(req: AgentRequest):
    """
    Get the current observation without taking an action.
    """
    if req.agent_name not in sessions:
        raise HTTPException(
            status_code=400,
            detail=f"No session for agent '{req.agent_name}'. Call /reset first.",
        )
    env_instance = sessions[req.agent_name]
    obs = env_instance.state()
    return ObservationResponse(observation=obs["observation"])
