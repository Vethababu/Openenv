from pydantic import BaseModel, Field
from typing import Dict, Any
import yaml

with open("openenv.yaml", "r") as f:
    SPEC = yaml.safe_load(f)


class ConfigRequest(BaseModel):
    agent_name: str = Field(..., description="Unique session/agent ID")
    task: str = Field(..., description="Task name: code_easy | code_medium | sys_hard")


class AgentRequest(BaseModel):
    agent_name: str = Field(..., description="Unique session/agent ID")


class ObservationResponse(BaseModel):
    observation: Dict[str, Any]


class StepRequest(BaseModel):
    agent_name: str = Field(..., description="Unique session/agent ID")
    action: str = Field(..., description="Action string from the task's action_space")


class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]
