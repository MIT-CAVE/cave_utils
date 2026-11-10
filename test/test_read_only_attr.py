"""
Coverage for the props that accept the `readOnly` attribute, which are the ones
whose UI honors it: `"text"`, `"date"`, `"num"` (`"field"` variant, or none) and
`"selector"` (`"combobox"`, `"comboboxMulti"` and `"dualList"` variants).

Fixed as part of MIT-CAVE/cave_static#718, where `date` and `num` props were
reported as having an unknown `readOnly` field.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}
OPTIONS = {"a": {"name": "A"}, "b": {"name": "B"}}


def validate_prop(prop, value):
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {"x": {"name": "X", **prop}},
                    "values": {"x": value},
                }
            },
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


@pytest.mark.parametrize(
    "prop, value",
    [
        ({"type": "text"}, "a"),
        ({"type": "date", "variant": "date"}, "2026-07-09"),
        ({"type": "date", "variant": "time"}, "09:30:00"),
        ({"type": "date", "variant": "datetime"}, "2026-07-09T09:00:00"),
        ({"type": "num"}, 1),
        ({"type": "num", "variant": "field"}, 1),
        ({"type": "selector", "variant": "combobox", "options": OPTIONS}, ["a"]),
        ({"type": "selector", "variant": "comboboxMulti", "options": OPTIONS}, ["a"]),
        ({"type": "selector", "variant": "dualList", "options": OPTIONS}, ["a"]),
    ],
)
def test_read_only_is_accepted(prop, value):
    assert validate_prop({**prop, "readOnly": True}, value) == []


@pytest.mark.parametrize(
    "prop, value",
    [
        ({"type": "num", "variant": "slider", "minValue": 0, "maxValue": 2}, 1),
        ({"type": "toggle"}, True),
        ({"type": "selector", "options": OPTIONS}, ["a"]),
        ({"type": "selector", "variant": "radio", "options": OPTIONS}, ["a"]),
    ],
)
def test_read_only_is_unknown_elsewhere(prop, value):
    log = validate_prop({**prop, "readOnly": True}, value)
    assert [entry["level"] for entry in log] == ["warning"]
    assert "readOnly" in log[0]["msg"]
