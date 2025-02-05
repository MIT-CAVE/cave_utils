
VERSION="3.1.0b1"
OLD_DOC_VERSIONS="3.0.0 2.2.1 2.1.2 2.0.5 2.3.0"

rm -r ./docs
python3 -m virtualenv venv
source venv/bin/activate

# If not in an venv, do not continue
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not in a virtual environment. Exiting."
    exit 1
fi

export version_options="$VERSION $OLD_DOC_VERSIONS"

# generate the docs for a version function:
function generate_docs() {
    INPUT_VERSION=$1
    pdoc --logo https://cave.mit.edu/wp-content/uploads/2022/12/MIT-CTL-CAVE-logo@4x.png --logo-link https://github.com/MIT-CAVE/cave_app -o ./docs/$INPUT_VERSION -t ./doc_template cave_utils
}

pip install -r requirements.txt
generate_docs ./
generate_docs $VERSION

for version in $OLD_DOC_VERSIONS; do
    pip install ./dist/cave_utils-$version-py3-none-any.whl
    generate_docs $version
done;

pip install -e .
