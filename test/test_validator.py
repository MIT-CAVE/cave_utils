from cave_utils import Validator, Socket
import os, importlib


def get_examples():
    examples_location = os.path.join(os.path.dirname(__file__), "api_examples")
    if not os.path.exists(examples_location):
        raise FileNotFoundError(f"Examples directory {examples_location} does not exist.")
    if not os.path.isdir(examples_location):
        raise NotADirectoryError(f"Examples location {examples_location} is not a directory.")
    return sorted(
        [
            i.replace(".py", "")
            for i in os.listdir(examples_location)
            if i.endswith(".py") and not i.startswith("__")
        ]
    )


def test_validator():
    success = True
    example_files = get_examples()
    for example_file in example_files:
        module_name = f"api_examples.{example_file}"
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        if hasattr(module, "execute_command"):
            example_data = module.execute_command(
                session_data={}, socket=Socket(silent=True), command="init"
            )
            x = Validator(session_data=example_data)
            if x.log.log != []:
                success = False
        else:
            raise AttributeError(
                f"Module {module_name} does not have an `execute_command` function."
            )
    assert success, (
        "Validator tests failed for one or more examples. "
        "Run Validator directly on the failing example to see the errors."
    )
