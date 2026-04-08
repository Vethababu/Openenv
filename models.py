from pydantic import BaseModel

class StepRequest(BaseModel):
    action: int
