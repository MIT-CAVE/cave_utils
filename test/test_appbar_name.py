"""
Test-only coverage for the optional `appBar.data.*.name` field: accepted on buttons and pages,
optional, and type checked.
"""

from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}


def validate_app_bar(items):
    session_data = {
        "settings": SETTINGS,
        "pages": {"data": {"page1": {"charts": {}}}},
        "appBar": {"data": items},
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


def app_bar_entries(log):
    return [entry for entry in log if "appBar" in str(entry.get("path", ""))]


def test_name_is_accepted_on_button_and_page():
    log = validate_app_bar(
        {
            "run": {
                "bar": "upperLeft",
                "icon": "md/MdBolt",
                "type": "button",
                "apiCommand": "run",
                "name": "Run the model",
            },
            "page1": {
                "bar": "upperLeft",
                "icon": "md/MdMap",
                "type": "page",
                "name": "Map",
            },
        }
    )
    assert app_bar_entries(log) == []


def test_name_is_optional():
    log = validate_app_bar(
        {"run": {"bar": "upperLeft", "icon": "md/MdBolt", "type": "button", "apiCommand": "run"}}
    )
    assert app_bar_entries(log) == []


def test_name_must_be_a_string():
    log = validate_app_bar(
        {
            "run": {
                "bar": "upperLeft",
                "icon": "md/MdBolt",
                "type": "button",
                "apiCommand": "run",
                "name": 5,
            }
        }
    )
    errors = [entry for entry in app_bar_entries(log) if entry.get("level") == "error"]
    assert len(errors) == 1
    assert "`name`" in errors[0]["msg"]
