Cave Utilities for the Cave App
==========
Basic utilities for the MIT Cave App. This package is intended to be used by the Cave App and the Cave API.

Setup
----------

Make sure you have Python 3.7.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install cave_utils
```

# Getting Started
## Example:
1. In your cave_app, update the following file:

    `cave_api/tests/test_init.py`
    ```
    from cave_api import execute_command
    from cave_utils.socket import Socket
    from cave_utils.validator import Validator


    init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

    x = Validator(init_session_data)

    x.print_errors()
    # x.print_warnings()
    # x.write_warnings('./warnings.txt')
    # x.write_errors('./errors.txt')
    ```

2. Run the following command:
    `cave test test_init.py`

# Live Utils Development 
1. In your cave_app, update the following file:

    `utils/run_server.sh`
    ```
    #!/bin/bash

    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    APP_DIR=$(dirname "$SCRIPT_DIR")

    pip install -e /cave_utils

    source ./utils/helpers/shell_functions.sh
    source ./utils/helpers/ensure_postgres_running.sh
    source ./utils/helpers/ensure_db_setup.sh

    python "$APP_DIR/manage.py" runserver 0.0.0.0:8000 2>&1 | pipe_log "INFO"
    ```

2. In your cave_app, set `LIVE_API_VALIDATION=True` in the `.env` file
    - This will validate your data every time an api command is called for each session
    - Outputs will be stored in `logs/validation/{session_name}.log`

3. Use the following command to run your cave_app:
    `cave run --docker-args "--volume {local_path_to_cave_utils}/cave_utils:/cave_utils"`
    
    As you edit cave_utils, the logs will be updated live