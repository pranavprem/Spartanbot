from controller import controller
from learn import main


def test_learn_py_loads_the_real_greensheet_and_can_answer():
    assert main() == 0
    reply = controller().find_solution("who is the instructor")
    lowered = reply.lower()
    assert "sithu" in lowered
    assert "custom solution" in lowered
