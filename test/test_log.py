from cave_utils.api import LogObject
import os


def test_log():
    x = LogObject()
    x.add(path=["test"], msg="Some test error", level="error")
    x.add(path=["test"], msg="Some test warning", level="warning")
    expected = {
        "log": [
            {"path": ["test"], "msg": "Some test error", "level": "error"},
            {"path": ["test"], "msg": "Some test warning", "level": "warning"},
        ]
    }
    assert x.__dict__ == expected, f"Expected {expected}, but got {x.__dict__}"
    x.write_logs(path="./logs/test_log.txt")
    if os.path.exists("./logs/test_log.txt"):
        os.remove("./logs/test_log.txt")
        if not os.listdir("./logs"):
            os.rmdir("./logs")
    else:
        raise FileNotFoundError("Log file was not created as expected.")
