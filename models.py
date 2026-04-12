from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import yaml
 
with open("openenv.yaml", "r") as f:
    SPEC = yaml.safe_load(f)
 
 
class ConfigRequest(BaseModel):
    agent_name: Optional[str] = Field(default="default_agent", description="Unique session/agent ID")
    task: Optional[str] = Field(default="code_easy", description="Task name: code_easy | code_medium | sys_hard")
 
 
class AgentRequest(BaseModel):
    agent_name: Optional[str] = Field(default="default_agent", description="Unique session/agent ID")
 
 
class ObservationResponse(BaseModel):
    observation: Dict[str, Any]
 
 
class StepRequest(BaseModel):
    agent_name: Optional[str] = Field(default="default_agent", description="Unique session/agent ID")
    action: Optional[str] = Field(default="no_change", description="Action string from the task's action_space")
 
 
class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]
 
