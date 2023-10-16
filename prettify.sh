# Change to the script directory
cd $(dirname "$0")
# Lint and Autoformat the code in place
# Remove unused imports
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r ./cave_utils
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r ./test
# Perform all other steps
black --config pyproject.toml ./cave_utils
black --config pyproject.toml ./test
