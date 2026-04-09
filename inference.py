import requests

URL = "http://localhost:8000"

def run():
    r = requests.post(f"{URL}/reset")
    total = 0

    for _ in range(50):
        action = 0
        res = requests.post(f"{URL}/step", json={"action": action}).json()
        total += res["reward"]

        if res["done"]:
            break

    print("Total reward:", total)

if __name__ == "__main__":
    run()
