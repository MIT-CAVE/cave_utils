"""
Dedicated negative-path coverage for the `"coordinate"` prop's attributes
added in MIT-CAVE/cave_static#716: `defaultZoom`/`minZoom`/`maxZoom`,
`maxBounds`, `pathColor` and `pathWeight`.

The happy path for these is already exercised indirectly by
`test_validator.py` via `test/api_examples/general_props_all_advanced.py`;
this file checks that out-of-range or malformed values are actually
rejected.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}
POINT = [[-71.092003, 42.360001]]
PATH = [[-71.092003, 42.360001], [-71.093003, 42.361001]]


def validate_coordinate(prop, value=POINT, variant="latLngMap"):
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {
                        "c": {
                            "name": "C",
                            "type": "coordinate",
                            "variant": variant,
                            **prop,
                        }
                    },
                    "values": {"c": value},
                }
            },
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


@pytest.mark.parametrize("field", ["defaultZoom", "minZoom", "maxZoom"])
def test_zoom_fields_reject_out_of_range(field):
    assert validate_coordinate({field: -1}) != []
    assert validate_coordinate({field: 23}) != []


@pytest.mark.parametrize("field", ["defaultZoom", "minZoom", "maxZoom"])
def test_zoom_fields_accept_in_range(field):
    assert validate_coordinate({field: 0}) == []
    assert validate_coordinate({field: 22}) == []


def test_max_bounds_rejects_malformed_shape():
    assert validate_coordinate({"maxBounds": [-71, 42, -70, 43]}) != []
    assert validate_coordinate({"maxBounds": [[-71, 42]]}) != []
    assert validate_coordinate({"maxBounds": [["west", 42], [-70, 43]]}) != []


def test_max_bounds_rejects_out_of_range_lng_lat():
    assert validate_coordinate({"maxBounds": [[-200, 42], [-70, 43]]}) != []
    assert validate_coordinate({"maxBounds": [[-71, -100], [-70, 43]]}) != []


def test_max_bounds_rejects_inverted_corners():
    # west >= east
    assert validate_coordinate({"maxBounds": [[-70, 42], [-71, 43]]}) != []
    # south >= north
    assert validate_coordinate({"maxBounds": [[-71, 43], [-70, 42]]}) != []


def test_max_bounds_accepts_valid_bounds():
    assert validate_coordinate({"maxBounds": [[-71.1, 42.3], [-71.0, 42.4]]}) == []


def test_path_color_rejects_invalid_string():
    assert validate_coordinate({"pathColor": "not-a-color"}, value=PATH, variant="latLngPath") != []


def test_path_color_accepts_valid_string():
    assert validate_coordinate({"pathColor": "#2e7d32"}, value=PATH, variant="latLngPath") == []


def test_path_weight_rejects_out_of_range():
    assert validate_coordinate({"pathWeight": 0}, value=PATH, variant="latLngPath") != []
    assert validate_coordinate({"pathWeight": 101}, value=PATH, variant="latLngPath") != []


def test_path_weight_accepts_in_range():
    assert validate_coordinate({"pathWeight": 1}, value=PATH, variant="latLngPath") == []
    assert validate_coordinate({"pathWeight": 100}, value=PATH, variant="latLngPath") == []


if __name__ == "__main__":
    pytest.main([__file__])
