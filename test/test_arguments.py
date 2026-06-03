import sys
from cave_utils import Arguments


def test_arguments():
    original_argv = sys.argv.copy()
    try:
        sys.argv = [
            "script_name.py",
            "--name",
            "value",
            "-v",
            "-flagonly",
            "pos1",
            "--another",
            "-x",
        ]
        args = Arguments()

        assert args.get_kwarg("name") == "value", "Failed to retrieve --name=value"
        assert (
            args.get_kwarg("nonexistent", "default") == "default"
        ), "Failed default value for missing kwarg"

        assert args.has_flag("v"), "Missing -v flag"
        assert args.has_flag("flagonly"), "Missing -flagonly flag"
        assert args.has_flag("x"), "Missing -x flag"

        assert "pos1" in args.other, "Missing positional argument 'pos1'"

        args.delete("name")
        assert args.get_kwarg("name") is None, "Failed to delete --name"

        args.delete("v", only_flag=True)
        assert not args.has_flag("v"), "Failed to delete -v flag"

        args.delete("pos1")
        assert "pos1" not in args.other, "Failed to delete positional argument 'pos1'"
    finally:
        sys.argv = original_argv
