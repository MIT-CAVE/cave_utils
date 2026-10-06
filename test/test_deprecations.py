"""
Test-only coverage for deprecated and undefined attributes.

These cases are kept out of `test/api_examples/` (which mirrors `cave_app`) so
that the examples never teach deprecated usage.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}
POINT = [[-71.092003, 42.360001]]
PATH = [[-71.092003, 42.360001], [-71.093003, 42.361001]]


def validate_global_output(prop):
    session_data = {
        "settings": SETTINGS,
        "globalOutputs": {
            "props": {
                "kpi": {
                    "name": "KPI",
                    "type": "num",
                    "variant": "icon",
                    "icon": "md/MdTrendingUp",
                    **prop,
                }
            },
            "values": {"kpi": 18},
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


def validate_coordinate(prop, value):
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {"c": {"name": "C", "type": "coordinate", **prop}},
                    "values": {"c": value},
                }
            },
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


def test_draggable_deprecated_alias_is_accepted():
    # `draggable` is deprecated in favor of `quickView`, but must still validate.
    assert validate_global_output({"draggable": True}) == []


def test_quick_view_is_accepted():
    assert validate_global_output({"quickView": True}) == []


def test_lat_lng_input_alias_behaves_like_lat_lng_map():
    # `latLngInput` is a deprecated alias of `latLngMap`: single points are valid, paths are not.
    assert validate_coordinate({"variant": "latLngInput"}, POINT) == []
    assert validate_coordinate({"variant": "latLngInput"}, PATH) != []
    assert validate_coordinate({"variant": "latLngMap"}, PATH) != []


def test_coordinate_default_variant_is_lat_lng_map():
    # With no `variant`, the default must behave like `latLngMap`, not `latLngPath`.
    assert validate_coordinate({}, POINT) == []
    assert validate_coordinate({}, PATH) != []


def test_lat_lng_path_accepts_paths():
    # Sanity check that the path value is valid for the path variant.
    assert validate_coordinate({"variant": "latLngPath"}, PATH) == []


if __name__ == "__main__":
    pytest.main([__file__])
