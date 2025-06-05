#!/bin/bash
cd /app/

# Make a temp init.py that only has the content below the __README_CONTENT_IS_COPIED_ABOVE__ line
cp README.md cave_utils/__init__.py
sed -i '1s/^/\"\"\"\n/' cave_utils/__init__.py
echo "\"\"\"" >> cave_utils/__init__.py

echo "from .log import LogObject, LogHelper" >> cave_utils/__init__.py
echo "from .socket import Socket" >> cave_utils/__init__.py
echo "from .api_utils.validator import Validator" >> cave_utils/__init__.py
echo "from .arguments import Arguments" >> cave_utils/__init__.py
echo "from .geo_utils import GeoUtils" >> cave_utils/__init__.py


# Specify versions for documentation purposes
VERSION="3.2.0"
OLD_DOC_VERSIONS="3.2.0 3.1.0 3.0.0 2.3.0 2.2.1 2.1.2 2.0.5 1.6.1"
export version_options="$VERSION $OLD_DOC_VERSIONS"

# generate the docs for a version function:
function generate_docs() {
    INPUT_VERSION=$1
    if [ $INPUT_VERSION != "./" ]; then
        if [ $INPUT_VERSION != $VERSION ]; then
            pip install "./dist/cave_utils-$INPUT_VERSION.tar.gz"
        fi
    fi
    pdoc --logo https://cave.mit.edu/wp-content/uploads/2022/12/MIT-CTL-CAVE-logo@4x.png --logo-link https://github.com/MIT-CAVE/cave_app -o ./docs/$INPUT_VERSION -t ./doc_template cave_utils
}

# Generate the docs for the current version
generate_docs ./
generate_docs $VERSION

# Generate the docs for all the old versions
for version in $OLD_DOC_VERSIONS; do
    generate_docs $version
done;

# Reinstall the current package as an egg
pip install -e .
