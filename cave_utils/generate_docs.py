import importlib
import inspect
import pkgutil
import sys
from pathlib import Path


def _is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _render_module(mod) -> str:
    modname = mod.__name__
    lines = [f"MODULE: {modname}", "=" * (len(modname) + 8)]

    if mod.__doc__:
        lines += ["", mod.__doc__.strip()]

    # Module-level functions defined in this module (non-dunder)
    funcs = [
        (name, obj)
        for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if not _is_dunder(name) and obj.__module__ == modname
    ]
    if funcs:
        lines += ["", "FUNCTIONS", "---------"]
        for name, obj in funcs:
            sig = inspect.signature(obj)
            lines += ["", f"{name}{sig}"]
            if obj.__doc__:
                lines.append(obj.__doc__.strip())

    # Classes defined in this module
    classes = [
        (name, obj)
        for name, obj in inspect.getmembers(mod, inspect.isclass)
        if not _is_dunder(name) and obj.__module__ == modname
    ]
    if classes:
        lines += ["", "CLASSES", "-------"]
        for cname, cls in classes:
            lines += ["", f"class {cname}", "-" * (len(cname) + 6)]
            if cls.__doc__:
                lines.append(cls.__doc__.strip())

            # Methods: static, class, and instance — skip dunders
            for mname, mobj in inspect.getmembers(cls, predicate=callable):
                if _is_dunder(mname):
                    continue
                # Get the raw function for signature/docstring
                raw = cls.__dict__.get(mname)
                if raw is None:
                    continue
                if isinstance(raw, staticmethod):
                    func = raw.__func__
                    prefix = "staticmethod "
                elif isinstance(raw, classmethod):
                    func = raw.__func__
                    prefix = "classmethod "
                elif callable(raw):
                    func = raw
                    prefix = ""
                else:
                    continue
                try:
                    sig = inspect.signature(func)
                except (ValueError, TypeError):
                    sig = ""
                lines += ["", f"  {prefix}{mname}{sig}"]
                if func.__doc__:
                    # Indent docstring under the method
                    for dline in func.__doc__.strip().splitlines():
                        lines.append(f"    {dline}")

    return "\n".join(lines) + "\n"


def generate_docs(output_dir: str = "cave_utils_docs"):
    """
    Generate plain text documentation for all cave_utils modules.

    Recursively discovers all cave_utils submodules and writes one .txt file
    per module (skipping dunder methods) plus a README.txt index.

    Arguments:

    * **`output_dir`**: `[str]` = `"cave_utils_docs"` &rarr; Path to the output directory.
      Created if it does not exist.
    """
    import cave_utils

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    modules = []
    prefix = cave_utils.__name__ + "."

    for _importer, modname, _ispkg in pkgutil.walk_packages(
        path=cave_utils.__path__, prefix=prefix, onerror=lambda x: None
    ):
        # Skip private/internal submodules
        if any(part.startswith("_") for part in modname.split(".")):
            continue
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue

        filename = modname.replace(".", "_") + ".txt"
        (out / filename).write_text(_render_module(mod))
        modules.append((modname, filename))

    # Write the project README from the cave_utils package docstring
    if cave_utils.__doc__:
        (out / "PROJECT_README.md").write_text(cave_utils.__doc__.strip() + "\n")

    lines = ["cave_utils Documentation", ""]
    lines.append("  Project README: ./PROJECT_README.md")
    for modname, filename in sorted(modules):
        lines.append(f"  {modname}: ./{filename}")
    lines.append("")
    (out / "README.txt").write_text("\n".join(lines))

    # print(f"Docs written to: {out.resolve()}")


def _cli():
    generate_docs(sys.argv[1] if len(sys.argv) > 1 else "cave_utils_docs")
