TASKS = {
    "code_easy": {
        "buggy_code": "def add(a, b):\n    print('wrong')\n    return a",
        "tests": [
            "add(1,2) == 3",
            "add(0,0) == 0",
            "add(-1,1) == 0"
        ]
    },
    "code_medium": {
        "buggy_code": "def factorial(n):\n    if n == 0: return 1\n    return n * factorial(n-1 +1)",
        "tests": [
            "factorial(0) == 1",
            "factorial(1) == 1",
            "factorial(5) == 120",
            "factorial(3) == 6"
        ]
    },
    "sys_hard": {
        "goal": "numpy installed: numpy.py exists with 'import numpy' and numpy in requirements.txt",
        "init_files": {
            "requirements.txt": "fastapi\nuvicorn"
        }
    }
}
