# Traffic AI OpenEnv

Real-world traffic signal optimization environment.

## Observation
lane1 cars  
lane2 cars  
light status  
emergency vehicle  

## Actions
0 = keep light  
1 = switch light  

## Reward
Negative of total waiting cars

## Run
uvicorn app:app --reload
