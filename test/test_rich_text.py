"""
Coverage for the generic `richText` key (MIT-CAVE/cave_static#655).

`richText` is handled generically (like `order` and `timeValues`): it is
accepted next to the data of any API item and must be a boolean.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}


def validate_pane(prop=None, layout=None, pane=None, value="a"):
    prop = prop or {}
    layout = layout or {}
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {"x": {"name": "X", "type": "text", **prop}},
                    "values": {"x": value},
                    **layout,
                    **(pane or {}),
                }
            },
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


@pytest.mark.parametrize("richText", [True, False])
def test_rich_text_is_accepted_on_a_prop(richText):
    assert validate_pane(prop={"richText": richText}) == []


@pytest.mark.parametrize("richText", [True, False])
def test_rich_text_is_accepted_on_layout_grids_and_items(richText):
    layout = {
        "layout": {
            "type": "grid",
            "richText": richText,
            "data": {"i": {"type": "item", "itemId": "x", "richText": not richText}},
        }
    }
    assert validate_pane(layout=layout) == []


def test_rich_text_is_accepted_on_prop_options():
    prop = {
        "type": "selector",
        "variant": "dropdown",
        "options": {"a": {"name": "**A**", "richText": True}},
    }
    assert validate_pane(prop={**prop, "richText": True}, value=["a"]) == []


def test_rich_text_unset_is_valid():
    assert validate_pane() == []


@pytest.mark.parametrize("richText", ["yes", 1, 0.5, [True], {"a": True}])
def test_rich_text_must_be_a_boolean(richText):
    log = validate_pane(prop={"richText": richText})
    assert len(log) == 1
    assert log[0]["path"] == ["panes", "data", "p", "props", "x", "richText"]
    assert "must be a boolean" in log[0]["msg"]


def test_rich_text_does_not_trigger_unknown_field_warnings():
    log = validate_pane(
        prop={"richText": True},
        layout={"layout": {"type": "grid", "richText": True}},
    )
    assert not any("Unknown Fields" in entry["msg"] for entry in log)
