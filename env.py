from typing import Dict, Any
from tasks import TASKS
from grader import grade_code_easy, grade_code_medium, grade_sys_hard
import copy


class CodeEasyEnv:
    """Easy code debug: fix syntax then logic then add test."""

    def __init__(self, task_config: Dict[str, Any]):
        self.buggy_code = task_config.get("buggy_code", "def add(a, b):\n    return a")
        self.tests = task_config.get("tests", [])
        self.error = "SyntaxError: unexpected EOF"
        self.tests_passed = 0
        self.max_tests = 3
        self.stage = 0  # 0: syntax, 1: logic, 2: full
        self.steps = 0
        self.max_steps = 15
        self._done = False

    def reset(self, config: Dict[str, Any] = {}) -> Dict[str, Any]:
        task = config.get("task", "code_easy")
        task_config = TASKS.get(task, {})
        self.__init__(task_config)
        return {"observation": self._obs()}

    def state(self) -> Dict[str, Any]:
        return {"observation": self._obs()}

    def step(self, action: str) -> Dict[str, Any]:
        info = {}

        # Already done: return terminal state
        if self._done:
            info["score"] = grade_code_easy(self.tests_passed, self.max_tests)
            return {
                "observation": self._obs(),
                "reward": 0.0,
                "done": True,
                "info": info,
            }

        reward = -0.05  # living penalty

        if action == "no_change":
            pass  # no reward change
        elif action == "fix_syntax" and self.stage == 0:
            self.error = ""
            self.tests_passed = 1
            self.stage = 1
            reward += 0.3
        elif action == "fix_logic" and self.stage == 1:
            self.tests_passed = 2
            self.stage = 2
            reward += 0.4
        elif action == "add_test" and self.stage == 2:
            self.tests_passed = 3
            reward += 0.3
        else:
            reward -= 0.1  # wrong action penalty

        self.steps += 1

        # Evaluate done AFTER incrementing steps
        self._done = (self.tests_passed == self.max_tests) or (self.steps >= self.max_steps)

        if self._done:
            info["score"] = grade_code_easy(self.tests_passed, self.max_tests)

        return {
            "observation": self._obs(),
            "reward": round(reward, 4),
            "done": self._done,
            "info": info,
        }

    def _obs(self) -> Dict[str, Any]:
        return {
            "code_snippet": self.buggy_code[:200],
            "error": self.error,
            "tests_passed": self.tests_passed,
            "max_tests": self.max_tests,
            "stage": self.stage,
            "steps_remaining": self.max_steps - self.steps,
        }


class CodeMediumEnv:
    """Medium: more stages, off-by-one/recursive bug, efficiency bonus."""

    def __init__(self, task_config: Dict[str, Any]):
        self.buggy_code = task_config.get(
            "buggy_code",
            "def factorial(n):\n    if n == 0: return 1\n    return n * factorial(n-1 +1)",
        )
        self.tests = task_config.get("tests", [])
        self.error = "RecursionError: maximum recursion depth exceeded"
        self.tests_passed = 0
        self.max_tests = 4
        self.stage = 0  # 0: syntax, 1: logic, 2: refactor, 3: done
        self.steps = 0
        self.max_steps = 20
        self._done = False

    def reset(self, config: Dict[str, Any] = {}) -> Dict[str, Any]:
        task = config.get("task", "code_medium")
        task_config = TASKS.get(task, {})
        self.__init__(task_config)
        return {"observation": self._obs()}

    def state(self) -> Dict[str, Any]:
        return {"observation": self._obs()}

    def step(self, action: str) -> Dict[str, Any]:
        info = {}

        if self._done:
            info["score"] = grade_code_medium(
                self.tests_passed, self.max_tests, self.steps, self.max_steps
            )
            return {
                "observation": self._obs(),
                "reward": 0.0,
                "done": True,
                "info": info,
            }

        reward = -0.05  # living penalty

        if action == "no_change":
            pass
        elif action == "fix_syntax" and self.stage == 0:
            self.error = ""
            self.tests_passed = 1
            self.stage = 1
            reward += 0.2
        elif action == "fix_logic" and self.stage == 1:
            self.tests_passed = 2
            self.stage = 2
            reward += 0.3
        elif action == "refactor" and self.stage == 2:
            self.tests_passed = 4
            self.stage = 3
            reward += 0.5
        else:
            reward -= 0.1

        self.steps += 1
        self._done = (self.tests_passed == self.max_tests) or (self.steps >= self.max_steps)

        if self._done:
            info["score"] = grade_code_medium(
                self.tests_passed, self.max_tests, self.steps, self.max_steps
            )

        return {
            "observation": self._obs(),
            "reward": round(reward, 4),
            "done": self._done,
            "info": info,
        }

    def _obs(self) -> Dict[str, Any]:
        return {
            "code_snippet": self.buggy_code[:200],
            "error": self.error,
            "tests_passed": self.tests_passed,
            "max_tests": self.max_tests,
            "stage": self.stage,
            "steps_remaining": self.max_steps - self.steps,
        }


class SysHardEnv:
    """Hard system ops: simulate filesystem/CLI task."""

    def __init__(self, task_config: Dict[str, Any]):
        # Deep copy init_files so resets are clean
        self.files: Dict[str, str] = copy.deepcopy(
            task_config.get("init_files", {"requirements.txt": "fastapi\nuvicorn"})
        )
        self.cur_dir = "/app"
        self.task_goal: str = task_config.get(
            "goal",
            "numpy installed: numpy.py exists with 'import numpy' and numpy in requirements.txt",
        )
        self.commands_log = []
        self.progress = 0.0
        self.steps = 0
        self.max_steps = 25
        self._done = False

    def reset(self, config: Dict[str, Any] = {}) -> Dict[str, Any]:
        task = config.get("task", "sys_hard")
        task_config = TASKS.get(task, {})
        self.__init__(task_config)
        return {"observation": self._obs()}

    def state(self) -> Dict[str, Any]:
        return {"observation": self._obs()}

    def step(self, action: str) -> Dict[str, Any]:
        info = {}
        self.commands_log.append(action)

        if self._done:
            info["score"] = grade_sys_hard(self.progress)
            return {
                "observation": self._obs(),
                "reward": 0.0,
                "done": True,
                "info": info,
            }

        reward = -0.05  # living penalty

        if action == "ls":
            reward = 0.05  # small info-gain reward
        elif action == "create_file":
            if "numpy.py" not in self.files:
                self.files["numpy.py"] = "import numpy"
                self.progress = min(self.progress + 0.5, 1.0)
                reward = 0.5
            else:
                reward -= 0.05  # already exists
        elif action == "pip_install":
            req = self.files.get("requirements.txt", "")
            if "numpy" not in req:
                self.files["requirements.txt"] = req + "\nnumpy"
                self.progress = min(self.progress + 0.5, 1.0)
                reward = 0.5
            else:
                reward -= 0.05  # already installed
        elif action == "cd":
            reward = 0.0  # neutral navigation
        else:
            reward -= 0.1  # unknown action

        self.steps += 1
        self._done = (self.progress >= 1.0) or (self.steps >= self.max_steps)

        if self._done:
            info["score"] = grade_sys_hard(self.progress)

        return {
            "observation": self._obs(),
            "reward": round(reward, 4),
            "done": self._done,
            "info": info,
        }

    def _obs(self) -> Dict[str, Any]:
        # Show full file contents (truncated per file, not the goal)
        files_str = "; ".join([f"{k}:{v[:30]}" for k, v in self.files.items()])
        return {
            "cur_dir": self.cur_dir,
            "files": files_str,
            "task_goal": self.task_goal,  # full goal, not truncated
            "progress": round(self.progress, 4),
            "steps_remaining": self.max_steps - self.steps,
        }


class OpenEnvRegistry:
    @staticmethod
    def create(task: str, config: Dict[str, Any] = {}) -> Any:
        # Always pull task_config from TASKS, not from the raw request config
        task_config = TASKS.get(task, {})
        if "code_easy" in task:
            return CodeEasyEnv(task_config)
        elif "code_medium" in task:
            return CodeMediumEnv(task_config)
        elif "sys_hard" in task:
            return SysHardEnv(task_config)
        raise ValueError(f"Unknown task: {task}. Available: code_easy, code_medium, sys_hard")


# Backward compat
def get_env(task: str, config: Dict[str, Any] = {}):
    return OpenEnvRegistry.create(task, config)
