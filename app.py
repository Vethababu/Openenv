from fastapi import FastAPI
from env import TrafficEnv
from models import StepRequest, ResetResponse, StepResponse, Observation, EnvSpec
import yaml

app = FastAPI()
env = TrafficEnv()

@app.post("/reset", response_model=ResetResponse)
def reset():
    return env.reset()

@app.post("/step", response_model=StepResponse)
def step(req: StepRequest):
    return env.step(req.action)

@app.get("/state", response_model=Observation)
def state():
    return env.state()

@app.get("/spec", response_model=EnvSpec)
def spec():
    with open('openenv.yaml', 'r') as f:
        spec_dict = yaml.safe_load(f)
    return EnvSpec(**spec_dict)