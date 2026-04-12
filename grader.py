def grade_code_easy(tests_passed: int, max_tests: int) -> float:
    """Score 0.0 (no tests) to 1.0 (all tests passed)."""
    if max_tests <= 0:
        return 0.0
    return round(float(tests_passed) / float(max_tests), 4)


def grade_code_medium(tests_passed: int, max_tests: int, steps_used: int = 0, max_steps: int = 20) -> float:
    """
    Score 0.0 to 1.0.
    Base score: tests_passed / max_tests (up to 0.85)
    Efficiency bonus: up to 0.15 for finishing quickly
    """
    if max_tests <= 0:
        return 0.0
    base = (float(tests_passed) / float(max_tests)) * 0.85
    if tests_passed == max_tests and steps_used > 0:
        efficiency = max(0.0, 1.0 - (steps_used / max_steps))
        bonus = efficiency * 0.15
    else:
        bonus = 0.0
    return round(base + bonus, 4)


def grade_sys_hard(progress: float) -> float:
    """
    Score 0.0 to 1.0 based on progress.
    Partial credit: 0.5 for partial completion, 1.0 for full.
    """
    progress = max(0.0, min(1.0, float(progress)))
    return round(progress, 4)
