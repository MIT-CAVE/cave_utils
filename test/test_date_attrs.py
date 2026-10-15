"""
Dedicated coverage for the `"date"` prop's attributes added in
MIT-CAVE/cave_static#718: `label`, `minDate`/`maxDate`, `minTime`/`maxTime`,
`minDateTime`/`maxDateTime`, `timezone` and `disablePast`/`disableFuture`.

Bounds accept several formats, while the prop's value stays strict. A value
outside of its bounds is reported as a warning.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}
VALUES = {"date": "2026-07-09", "datetime": "2026-07-09T09:00:00", "time": "09:30:00"}


def validate_date(prop, variant="date", value=None):
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {"d": {"name": "D", "type": "date", "variant": variant, **prop}},
                    "values": {"d": value or VALUES[variant]},
                }
            },
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


@pytest.mark.parametrize("variant", ["date", "datetime", "time"])
def test_label_and_flags_are_accepted(variant):
    prop = {"label": "When", "disablePast": True, "disableFuture": False}
    assert validate_date(prop, variant) == []


@pytest.mark.parametrize(
    "bounds",
    [
        {"minDate": "2026-07-01", "maxDate": "2026-07-31"},
        {"minDate": "2026-07-01T00:00:00", "maxDate": "2026-07-31 12:00:00"},
    ],
)
@pytest.mark.parametrize("variant", ["date", "datetime"])
def test_date_bounds_accept_flexible_formats(bounds, variant):
    assert validate_date(bounds, variant) == []


@pytest.mark.parametrize(
    "bounds",
    [
        {"minTime": "08:00", "maxTime": "17:00:00"},
        {"minTime": "2026-07-01T08:00:00", "maxTime": "2026-07-01 17:00:00"},
    ],
)
@pytest.mark.parametrize("variant", ["time", "datetime"])
def test_time_bounds_accept_flexible_formats(bounds, variant):
    assert validate_date(bounds, variant) == []


@pytest.mark.parametrize("field", ["minDate", "maxDate"])
def test_date_bounds_reject_unparseable_strings(field):
    assert validate_date({field: "07/09/2026"}) != []


@pytest.mark.parametrize("field", ["minTime", "maxTime"])
def test_time_bounds_reject_unparseable_strings(field):
    assert validate_date({field: "9am"}, "time") != []


def test_date_bounds_reject_inverted_range():
    assert validate_date({"minDate": "2026-07-31", "maxDate": "2026-07-01"}) != []


def test_time_bounds_reject_inverted_range():
    assert validate_date({"minTime": "17:00", "maxTime": "08:00"}, "time") != []


def test_date_bounds_ignore_time_part_when_comparing():
    bounds = {"minDate": "2026-07-09T23:00:00", "maxDate": "2026-07-09T01:00:00"}
    assert validate_date(bounds) == []


def test_time_bounds_are_rejected_on_date_variant():
    assert validate_date({"minTime": "08:00"}, "date") != []


def test_date_bounds_are_rejected_on_time_variant():
    assert validate_date({"minDate": "2026-07-01"}, "time") != []


@pytest.mark.parametrize("bound", ["2026-07-01T00:00:00", "2026-07-01 00:00:00"])
def test_datetime_bounds_accept_time_part(bound):
    assert validate_date({"minDateTime": bound}, "datetime") == []


@pytest.mark.parametrize("field", ["minDateTime", "maxDateTime"])
@pytest.mark.parametrize("bound", ["2026-07-01", "09:00", "07/01/2026"])
def test_datetime_bounds_reject_missing_time_part(field, bound):
    assert validate_date({field: bound}, "datetime") != []


def test_datetime_bounds_reject_inverted_range():
    bounds = {"minDateTime": "2026-07-10T00:00:00", "maxDateTime": "2026-07-01T00:00:00"}
    assert validate_date(bounds, "datetime") != []


@pytest.mark.parametrize("variant", ["date", "time"])
def test_datetime_bounds_are_rejected_on_other_variants(variant):
    assert validate_date({"minDateTime": "2026-07-01T00:00:00"}, variant) != []


@pytest.mark.parametrize(
    "variant, bounds",
    [
        ("date", {"minDate": "2026-07-10"}),
        ("date", {"maxDate": "2026-07-08"}),
        ("time", {"minTime": "10:00"}),
        ("time", {"maxTime": "09:00"}),
        ("datetime", {"minDate": "2026-07-10"}),
        ("datetime", {"maxTime": "08:00"}),
        ("datetime", {"minDateTime": "2026-07-09T09:00:01"}),
        ("datetime", {"maxDateTime": "2026-07-09T08:59:59"}),
    ],
)
def test_value_outside_of_bounds_warns(variant, bounds):
    log = validate_date(bounds, variant)
    assert [entry["level"] for entry in log] == ["warning"]


@pytest.mark.parametrize(
    "variant, bounds",
    [
        ("date", {"minDate": "2026-07-09", "maxDate": "2026-07-09"}),
        ("time", {"minTime": "09:30", "maxTime": "09:30:00"}),
        ("datetime", {"minDateTime": "2026-07-09T09:00:00", "maxDateTime": "2026-07-09 09:00:00"}),
    ],
)
def test_value_on_the_bounds_does_not_warn(variant, bounds):
    assert validate_date(bounds, variant) == []


def test_datetime_bound_differs_from_date_and_time_window():
    # 08:00 on a later day is outside of a daily `minTime` window...
    window = {"minDate": "2026-07-05", "minTime": "09:00"}
    assert validate_date(window, "datetime", value="2026-07-06T08:00:00") != []
    # ... but after a single `minDateTime` cutoff
    cutoff = {"minDateTime": "2026-07-05T09:00:00"}
    assert validate_date(cutoff, "datetime", value="2026-07-06T08:00:00") == []


@pytest.mark.parametrize("variant", ["date", "datetime", "time"])
@pytest.mark.parametrize("timezone", ["system", "UTC", "America/New_York", "Pacific/Kiritimati"])
def test_timezone_accepts_system_utc_and_iana_names(variant, timezone):
    assert validate_date({"timezone": timezone}, variant) == []


@pytest.mark.parametrize("timezone", ["Mars/Olympus_Mons", "EST+5", "", "../etc/passwd"])
def test_timezone_rejects_unknown_names(timezone):
    assert validate_date({"timezone": timezone}) != []
