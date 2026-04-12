def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (not 0.0, not 1.0)."""
    return round(max(0.01, min(0.99, float(score))), 4)
 
 
def grade_code_easy(tests_passed: int, max_tests: int) -> float:
    if max_tests <= 0:
        return 0.01
    raw = float(tests_passed) / float(max_tests)
    return _clamp(raw)
 
 
def grade_code_medium(tests_passed: int, max_tests: int, steps_used: int = 0, max_steps: int = 20) -> float:
    if max_tests <= 0:
        return 0.01
    base = (float(tests_passed) / float(max_tests)) * 0.85
    if tests_passed == max_tests and steps_used > 0:
        efficiency = max(0.0, 1.0 - (steps_used / max_steps))
        bonus = efficiency * 0.15
    else:
        bonus = 0.0
    return _clamp(base + bonus)
 
 
def grade_sys_hard(progress: float) -> float:
    progress = max(0.0, min(1.0, float(progress)))
    return _clamp(progress)
