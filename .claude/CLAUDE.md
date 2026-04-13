# CAVE Utils: Claude Instructions

## Project Purpose

`cave_utils` is a Python utility library for the CAVE App framework. Its two main jobs are:
1. **API validation** — validate `session_data` dicts against the CAVE API spec, with structured error/warning logging
2. **Builders** — helper classes for constructing common data structures (hierarchical groups, date groups)

It also exposes minor utilities: `GeoUtils`, `CustomCoordinateSystem`, `Arguments`, `Socket`, `LogObject`.

---

## Directory Layout (relevant files only)

```
cave_utils/
  __init__.py                  # Public exports: Validator, LogObject, Socket, etc.
  api/
    __init__.py                # Root validator class; orchestrates all top-level key validation
    appBar.py                  # appBar validator
    draggables.py              # draggables validator
    extraKwargs.py             # extraKwargs validator
    globalOutputs.py           # globalOutputs validator
    groupedOutputs.py          # groupedOutputs validator
    mapFeatures.py             # mapFeatures validator
    maps.py                    # maps validator
    pages.py                   # pages validator
    panes.py                   # panes validator
    settings.py                # settings validator
  api_utils/
    validator_utils.py         # ApiValidator base class + CustomKeyValidator
    validator.py               # Top-level Validator class (entry point for users)
    general.py                 # Shared spec items (e.g. `props` class)
  builders/
    groups.py                  # GroupsBuilder, DateGroupsBuilder
test/
  api_examples/                # One .py per API feature; each has execute_command()
  test_validator.py            # Iterates all api_examples, validates with Validator
  test_builders_*.py           # Unit tests for builders
  test_*.py                    # Unit tests for other modules
utils/
  prettify.sh                  # autoflake + black
  test.sh                      # Runs all test/*.py files
pyproject.toml                 # black config: line-length=100, target py311
```

---

## Development Commands

All commands use Docker. Do **not** run pytest or python directly — always use `./run.sh`:

| Command | What it does |
|---|---|
| `./run.sh test` | Run all tests inside Docker |
| `./run.sh prettify` | Format with autoflake + black (line-length=100) |
| `./run.sh docs` | Regenerate pdoc documentation |
| `./run.sh` | Drop into a Docker shell |

> **Note:** `./run.sh` requires a TTY. In non-interactive contexts (CI, background tasks) it will fail with "the input device is not a TTY". Ask the user to run it themselves.

**Test runner details** (`utils/test.sh`): Executes every `.py` file in `/app/test/` with Python. Each file prints `Tests: Passed!` or `Tests: Failed!` and exits.

**`test_validator.py` specifically**: Dynamically imports every file in `test/api_examples/`, calls `execute_command(session_data={}, socket=Socket(silent=True), command="init")`, and checks that `Validator(session_data=result).log.log == []` (empty log = no errors/warnings).

---

## API Validator Architecture

### Key Classes

**`ApiValidator`** (`api_utils/validator_utils.py`) — base class for all validators:
- `spec(**kwargs)` — static method. Declare expected fields as parameters (with types and defaults). Return `{"kwargs": kwargs, "accepted_values": {field: [valid, values]}}`. Any key in `accepted_values` is automatically checked against the corresponding field in `self.data`. Unknown fields land in `kwargs` and trigger a warning.
- `__extend_spec__(**kwargs)` — override for cross-field or nested validation that can't be expressed in `spec()` alone.
- `__error__(msg, path=[])` / `__warn__(msg, path=[])` — log errors/warnings; `path` is relative to this validator's prepend_path.
- Helper methods: `__check_type__`, `__check_type_list__`, `__check_type_dict__`, `__check_subset_valid__`, `__prevent_subset_collision__`, `__check_color_string_valid__`, `__check_pixel_string_valid__`, `__check_url_valid__`, `__check_date_valid__`, `__check_coord_path_valid__`

**`CustomKeyValidator`** (`api_utils/validator_utils.py`) — validates an arbitrary-keyed dict where every value must be a dict and conform to a given validator class. Usage:
```python
CustomKeyValidator(
    data=self.data.get("someKey", {}),
    log=self.log,
    prepend_path=["someKey"],
    validator=MyStar_Validator,   # required kwarg
    # any extra kwargs are forwarded to MyStar_Validator
)
```
The current field's key is passed to the child validator as `CustomKeyValidatorFieldId`.

### Adding a New Top-Level API Key

1. Create `cave_utils/api/{key}.py` with validator class(es) following the pattern below.
2. In `cave_utils/api/__init__.py`:
   - Add import: `from cave_utils.api.{key} import {key}`
   - Add `{key}: dict = dict()` parameter to `Root.spec()`
   - Add docstring entry for it in `Root.spec()`
   - Add validation call in `Root.__extend_spec__()` (following the `if data != {}:` guard pattern)

### Validator Class Pattern

```python
"""
Module docstring describing this API section.
"""

from cave_utils.api_utils.validator_utils import ApiValidator, CustomKeyValidator
import type_enforced

@type_enforced.Enforcer
class myKey(ApiValidator):
    """
    Located under the path **`myKey`**.
    """

    @staticmethod
    def spec(requiredField: str, optionalField: int = 0, **kwargs):
        """
        Arguments:

        * **`requiredField`**: `[str]` &rarr; Description.
        * **`optionalField`**: `[int]` = `0` &rarr; Description.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "someField": ["valid", "values"],
            },
        }

    def __extend_spec__(self, **kwargs):
        # Cross-field or nested validation here
        CustomKeyValidator(
            data=self.data.get("data", {}),
            log=self.log,
            prepend_path=["data"],
            validator=myKey_data_star,
            **kwargs,
        )
```

**Rules:**
- Always decorate with `@type_enforced.Enforcer` — it enforces parameter types at call time.
- Always accept `**kwargs` in `spec()` and return it as `"kwargs"` — unknown fields are warned automatically.
- Use `None` as default for optional fields that should have no effect when absent (e.g. `myField: str | None = None`).
- Nested dicts with fixed structure → create a sub-validator class and instantiate it in `__extend_spec__`.
- Nested dicts with arbitrary keys → use `CustomKeyValidator`.

### `generic` Key Handling

`__genericKeyValidation__()` in `ApiValidator` automatically handles two special keys before `spec()` runs:
- **`timeValues`**: A list or int-keyed dict of partial data dicts for time-series animation. Validated against `settings.time.timeLength`. The first timeValue is merged into `self.data` so nested validators see it.
- **`order`**: A dict of lists defining display ordering for sibling dicts. Automatically validated against present keys.

These do **not** need to be declared in `spec()`.

### kwargs Threading

`Root.__extend_spec__()` passes these special kwargs down the validation tree:
- `timeLength` — extracted from `settings.time.timeLength`; needed to validate `timeValues`
- `root_data` — the full session_data dict; used by `settings_sync_star`
- `mapFeatures_feature_props` — props per map feature; used by maps
- `maps_validMapIds`, `globalOuputs_validPropIds`, `groupedOutputs_validLevelIds`, `groupedOutputs_validStatIds`, `groupedOutputs_validDatasetIds` — cross-reference IDs for pages
- `page_validPageIds`, `pane_validPaneIds` — cross-reference IDs for appBar

---

## Test API Examples

`test/api_examples/` contains focused examples, each exporting:
```python
def execute_command(session_data, socket, command):
    # Build and return session_data dict
    return session_data
```

When adding a new top-level key or feature, add or update a file in `test/api_examples/` to cover it. The validator test automatically picks up any `.py` file in that directory that has `execute_command`.

**`kitchen_sink.py`** is the comprehensive example that exercises most features at once: it's a good reference for overall structure.

These are pulled in from the cave_app examples so do not modify them. If you want to have custom tests, create a different file in `test` that handes these tests separately from the main validator test.

---

## Coding Conventions

- **Line length**: 100 characters (black config in `pyproject.toml`)
- **Python version**: 3.11+ (use `str | None` union syntax, not `Optional[str]`)
- **Formatting**: Always run `./run.sh prettify` before committing
- **Docstrings**: API validators use a specific markdown-style format for pdoc generation. Match the existing format exactly (bold param names, type annotations, `&rarr;`, `**See**:`, `**Note**:`, `**Notes**:`, `**Accepted Values**:` etc.)
- **No unnecessary abstractions**: Don't create shared helpers unless the same logic appears 3+ times across different files.

---

## Detailed Overview

The Cave Utils project is part of the larger CAVE App framework, which is designed to facilitate the creation of interactive data applications. The codebase is organized into several directories, each serving a specific purpose in the development and operation of CAVE projects.

Cave Utils is designed to be an easy-to-integrate library that provides utilities commonly used across different Cave applications, such as validation and logging. It also serves to provide automated documentation and testing for CAVE projects.

For the main utility code, see the `cave_utils` directory, which contains the core logic and functionality for the utilities provided by this package. This includes functions and classes for validation, logging, and other common tasks that are essential for building and maintaining CAVE applications.

In the `cave_utils` directory, you will find various modules that handle different aspects of utility functions, such as:
- `cave_utils/api/`: This module contains all the validator endpoints for validating and documenting the CAVE API spec. In this directory, all API top level keys are defined as separate files with their own validation logic and documentation baked in. This allows for easy maintenance and scalability of the API validation logic as the CAVE projects evolve and grow in complexity.
- `cave_utils/api_utils/`: This module contains utility functions that are used across the API validation logic. These functions may include common validation patterns, helper functions for processing API data, and other utilities that support the API validation process.
- `cave_utils/builders`: This module contains builder functions that are used to construct various components of the CAVE applications, such as charts, maps, and other visualizations. These builders provide a standardized way to create and configure these components given standard input structures, making it easier for developers to build out their CAVE projects with consistent and reusable code.
- `cave_utils/arguments.py`: This file contains the argument parsing logic for the CAVE utilities, allowing developers to easily handle command-line arguments for various other utility uses.
- `cave_utils/custom_coordinates.py`: This file contains logic for handling custom coordinate systems in map visualizations within CAVE projects. It provides functions and classes for defining and working with custom coordinate systems, allowing developers to create maps that are tailored to their specific data and visualization needs.
- `cave_utils/geo_utils.py`: This file contains utility functions for working with geographic data in CAVE projects. It includes functions for processing and manipulating geographic data, such as calculating distances, converting between coordinate systems, and other common geographic operations that are essential for building map visualizations in CAVE applications.
- `cave_utils/log.py`: This file contains the logging configuration and utility functions for the CAVE utilities. It provides a standardized way to log messages and events within the CAVE applications, allowing developers to easily track and debug their code as they build and maintain their CAVE projects.
- `cave_utils/socket.py`: This file contains an empty socket object that can be used in testing to simulate websocket interactions without needing to set up actual websocket connections. This is useful for testing and development purposes, allowing developers to test their code that fires websocket messages to users without having to set up a full websocket environment. The socket object can be easily extended with additional functionality as needed for specific testing scenarios, providing a flexible and convenient tool for simulating websocket interactions in CAVE projects.

Testing:
- All tests are located in the `test` directory.
- Containerized testing: `./run.sh test` will run all tests in a docker container, which ensures a consistent testing environment and makes it easier to manage dependencies and configurations for testing across different systems.

Linting:

- Linting is always done with `./run.sh prettify` to ensure consistent formatting across the codebase. This command runs a prettify script that applies the desired code formatting rules to the entire codebase, making it easier to maintain a clean and readable code style throughout the project.

Other Instructions:

Ignore content in gitignored files like __pycache__, venv, .claude, *.egg-info, build, dist, etc. is not relevant to the codebase and should not be considered when making edits or suggestions.


---




## Release Process

1. Ensure all tests pass and code is prettified
2. Update `version` in both `pyproject.toml` and `setup.cfg`
3. Ensure all tests pass `./run.sh test`
4. Update the `./utils/docs.sh` script with the new version number and run it to regenerate the docs with the new version number in the API reference.
4. Build the docs `./run.sh docs` and verify the generated `docs/` looks correct

Python: **≥ 3.11** | Key deps: `pamda`, `type_enforced`
