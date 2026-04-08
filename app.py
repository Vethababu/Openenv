from fastapi import FastAPI
from env import TrafficEnv
from models import StepRequest

app = FastAPI()
env = TrafficEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(req: StepRequest):
    return env.step(req.action)

@app.get("/state")
def state():
    return env.state()
