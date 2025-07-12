#!/bin/bash
docker build . --tag "cave_utils" --quiet > /dev/null
# if an arg was passed: use it as an entrypoint
if [ -z "$1" ]; then
    docker run -it --rm \
        --volume "$(pwd):/app" \
        "cave_utils"
else
    docker run -it --rm \
        --volume "$(pwd):/app" \
        --entrypoint "/app/utils/$1.sh" \
        "cave_utils"
fi