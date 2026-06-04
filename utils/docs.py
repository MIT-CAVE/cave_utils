import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent.parent
cave_utils = root / "cave_utils" / "__init__.py"

VERSION = "3.5.7"
OLD_DOC_VERSIONS = ["3.4.4", "3.3.0", "3.2.0", "3.1.0", "3.0.0", "2.3.0", "2.2.1", "2.1.2", "2.0.5", "1.6.1"]

env = {
    **os.environ,
    "version_options": " ".join([VERSION] + OLD_DOC_VERSIONS),
}

# function generate_docs() {
#     INPUT_VERSION=$1
#     if [ $INPUT_VERSION != "./" ]; then
#         if [ $INPUT_VERSION != $VERSION ]; then
#             pip install "./dist/cave_utils-$INPUT_VERSION.tar.gz"
#         fi
#     fi
#     pdoc --logo https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/e/2085/files/2022/12/MIT-CTL-CAVE-logo@4x-e1702410588429-768x136.png --logo-link https://github.com/MIT-CAVE/cave_app -o ./docs/$INPUT_VERSION -t ./doc_template cave_utils
# }

logo_url = "https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/e/2085/files/2022/12/MIT-CTL-CAVE-logo@4x-e1702410588429-768x136.png"
logo_link = "https://github.com/MIT-CAVE/cave_app"


def generate_docs(version):
    out_dir = str(root / "docs" / version)
    template_dir = str(root / "doc_template")

    if version != "./" and version != VERSION:
        # Use an isolated environment per old version so their (older)
        # dependencies don't clobber the current venv.
        tarball = str(root / "dist" / f"cave_utils-{version}.tar.gz")
        subprocess.run(
            [
                "uv", "run", "--isolated",
                "--with", tarball,
                "--with", "pdoc",
                "pdoc", "-o", out_dir, "-t", template_dir, "cave_utils", "--logo", logo_url, "--logo-link", logo_link
            ],
            check=True,
            env=env,
            cwd=str(root),
        )
    else:
        subprocess.run(
            [sys.executable, "-m", "pdoc", "-o", out_dir, "-t", template_dir, "cave_utils", "--logo", logo_url, "--logo-link", logo_link],
            check=True,
            env=env,
        )


# Build __init__.py from README
readme = (root / "README.md").read_text()

imports = """
from .log import LogObject, LogHelper
from .socket import Socket
from .api_utils.validator import Validator
from .arguments import Arguments
from .geo_utils import GeoUtils
from .custom_coordinates import CustomCoordinateSystem
"""

cave_utils.write_text(f'"""\n{readme}\n"""\n{imports}\n')

generate_docs("./")
generate_docs(VERSION)
for version in OLD_DOC_VERSIONS:
    generate_docs(version)
