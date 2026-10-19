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
    # A `variant` of `None` is omitted, which defaults to `"date"`
    variant_field = {} if variant is None else {"variant": variant}
    session_data = {
        "settings": SETTINGS,
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "p", "pin": True}},
            "data": {
                "p": {
                    "name": "P",
                    "props": {"d": {"name": "D", "type": "date", **variant_field, **prop}},
                    "values": {"d": value or VALUES[variant or "date"]},
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


@pytest.mark.parametrize(
    "variant, view",
    [
        ("date", "year"),
        ("date", "day"),
        ("time", "minutes"),
        ("datetime", "hours"),
    ],
)
def test_default_view_is_accepted_among_the_default_views(variant, view):
    assert validate_date({"defaultView": view}, variant) == []


def test_default_view_is_accepted_among_the_provided_views():
    prop = {"views": ["year", "month", "day"], "defaultView": "month"}
    assert validate_date(prop) == []


@pytest.mark.parametrize(
    "variant, view",
    [
        ("date", "month"),  # Valid view name, but not in the default views
        ("time", "seconds"),
        ("datetime", "month"),
    ],
)
def test_default_view_must_be_among_the_available_views(variant, view):
    assert validate_date({"defaultView": view}, variant) != []


def test_default_view_must_be_among_the_provided_views():
    prop = {"views": ["year", "month", "day"], "defaultView": "hours"}
    assert validate_date(prop) != []


@pytest.mark.parametrize("variant, view", [("date", "hours"), ("time", "day"), ("date", "decade")])
def test_default_view_must_be_a_view_of_the_variant(variant, view):
    assert validate_date({"defaultView": view}, variant) != []


TIME_VIEWS = ["hours", "minutes", "seconds"]


@pytest.mark.parametrize("variant", ["time", "datetime"])
@pytest.mark.parametrize(
    "steps",
    [
        {"minutesStep": 15},
        {"hoursStep": 2, "minutesStep": 15},
        {"hoursStep": 1, "minutesStep": 1},
        {"hoursStep": 24, "minutesStep": 60},
    ],
)
def test_step_attrs_are_accepted(variant, steps):
    value = "2026-07-09T00:00:00" if variant == "datetime" else "00:00:00"
    assert validate_date(steps, variant, value=value) == []


def test_step_attrs_with_every_unit_are_accepted():
    prop = {"views": TIME_VIEWS, "hoursStep": 2, "minutesStep": 15, "secondsStep": 30}
    assert validate_date(prop, "time", value="10:30:30") == []


@pytest.mark.parametrize(
    "steps",
    [
        {"hoursStep": 5},
        {"minutesStep": 7},
        {"secondsStep": 0},
        {"minutesStep": -15},
        {"hoursStep": 48},
        {"secondsStep": 90},
    ],
)
def test_step_attrs_must_divide_their_unit(steps):
    prop = {"views": TIME_VIEWS, **steps}
    log = validate_date(prop, "time", value="00:00:00")
    assert "error" in [entry["level"] for entry in log]


@pytest.mark.parametrize(
    "steps",
    [{"minutesStep": 15.5}, {"minutesStep": "15"}, {"daysStep": 2}, {"timeSteps": {"minutes": 15}}],
)
def test_step_attrs_reject_malformed_entries(steps):
    assert validate_date(steps, "time", value="00:00:00") != []


def test_step_attrs_are_rejected_on_date_variant():
    assert validate_date({"minutesStep": 15}, "date") != []


@pytest.mark.parametrize(
    "steps, value",
    [
        ({"minutesStep": 15}, "10:07:00"),
        ({"hoursStep": 3}, "10:30:00"),
    ],
)
def test_value_off_step_warns(steps, value):
    log = validate_date(steps, "time", value=value)
    assert [entry["level"] for entry in log] == ["warning"]
    assert "Step" in log[0]["msg"]


def test_value_on_step_does_not_warn():
    prop = {"views": TIME_VIEWS, "hoursStep": 3, "minutesStep": 15, "secondsStep": 30}
    assert validate_date(prop, "time", value="09:45:30") == []


def test_step_of_unavailable_view_warns_without_checking_the_value():
    # `seconds` is not one of the default views, so the step can't be used
    log = validate_date({"secondsStep": 30}, "time", value="10:30:15")
    assert [entry["level"] for entry in log] == ["warning"]
    assert "no effect" in log[0]["msg"]


WEEKDAY_NOTATIONS = [
    ("Sunday", 0), ("sun", 0), ("SU", 0), (0, 0),
    ("Monday", 1), ("Mon", 1), ("mo", 1), (1, 1),
    ("Tuesday", 2), ("Tue", 2), ("Tu", 2),
    ("Wednesday", 3), ("Wed", 3), ("We", 3),
    ("Thursday", 4), ("Thu", 4), ("Th", 4),
    ("Friday", 5), ("Fri", 5), ("Fr", 5),
    ("Saturday", 6), ("Sat", 6), ("Sa", 6), (6, 6),
]  # fmt: skip
MONTH_NOTATIONS = [
    ("January", 1), ("jan", 1), (1, 1), ("February", 2), ("Feb", 2),
    ("March", 3), ("Mar", 3), ("April", 4), ("Apr", 4), ("May", 5), (5, 5),
    ("June", 6), ("Jun", 6), ("July", 7), ("Jul", 7), ("August", 8), ("Aug", 8),
    ("September", 9), ("Sep", 9), ("October", 10), ("Oct", 10),
    ("November", 11), ("Nov", 11), ("December", 12), ("Dec", 12), (12, 12),
]  # fmt: skip
# 2026-07-09 is a Thursday (4) in July (7). Every other date used below differs in all of them.
CALENDAR_KEYS = {
    "disabledWeekdays": (WEEKDAY_NOTATIONS, 4),
    "disabledMonths": (MONTH_NOTATIONS, 7),
}


@pytest.mark.parametrize("key", CALENDAR_KEYS)
def test_calendar_notations_are_accepted_and_match_the_value(key):
    notations, hit = CALENDAR_KEYS[key]
    for notation, index in notations:
        log = validate_date({key: [notation]}, "date")
        expected = ["warning"] if index == hit else []
        assert [entry["level"] for entry in log] == expected, (key, notation)


@pytest.mark.parametrize(
    "key, entry",
    [
        ("disabledWeekdays", 7),
        ("disabledWeekdays", -1),
        ("disabledWeekdays", True),
        ("disabledWeekdays", "Thur"),
        ("disabledWeekdays", "3"),
        ("disabledWeekdays", "tuesdays"),
        ("disabledMonths", 0),
        ("disabledMonths", 13),
        ("disabledMonths", True),
        ("disabledMonths", "Sept"),
        ("disabledMonths", "2026-12"),
        ("disabledMonths", "7"),
    ],
)
def test_unrecognized_calendar_entries_are_rejected(key, entry):
    log = validate_date({key: [entry]}, "date")
    assert "error" in [e["level"] for e in log]


@pytest.mark.parametrize(
    "key, entries",
    [
        ("disabledWeekdays", [0, "Mon", "Tuesday", "We", "thu", 5, "Sat"]),
        ("disabledMonths", list(range(1, 13))),
        (
            "disabledMonths",
            ["Jan", 2, "March", "Apr", "May", 6, "Jul", "Aug", "Sep", 10, 11, "December"],
        ),
    ],
)
def test_disabling_everything_is_an_error(key, entries):
    log = validate_date({key: entries}, "date")
    assert any(e["level"] == "error" and "every" in e["msg"] for e in log)


def test_repeated_entries_do_not_count_as_everything():
    assert [e["level"] for e in validate_date({"disabledWeekdays": [0, "Sun", "Su"] * 3})] == []


@pytest.mark.parametrize("variant", ["date", "datetime"])
def test_disabled_dates_and_years_are_accepted(variant):
    prop = {"disabledDates": ["2026-07-10", "2026-07-11T10:00:00", "2026-07-12 10:00:00"]}
    assert validate_date({**prop, "disabledYears": [2025, 2027]}, variant) == []


@pytest.mark.parametrize(
    "entry", ["07-10-2026", "2026/07/10", "2026-07", "2026-13-01", "10:00:00", ""]
)
def test_malformed_disabled_dates_are_rejected(entry):
    assert "error" in [e["level"] for e in validate_date({"disabledDates": [entry]})]


@pytest.mark.parametrize(
    "prop",
    [
        {"disabledDates": ["2026-07-09"]},
        {"disabledDates": ["2026-07-09T23:59:59"]},
        {"disabledYears": [2026]},
    ],
)
def test_value_on_a_disabled_date_or_year_warns(prop):
    log = validate_date(prop)
    assert [e["level"] for e in log] == ["warning"]
    assert "disabled" in log[0]["msg"]


def test_value_next_to_disabled_date_does_not_warn():
    assert (
        validate_date({"disabledDates": ["2026-07-08", "2026-07-10"], "disabledYears": [2025]})
        == []
    )


@pytest.mark.parametrize(
    "key, entry",
    [
        ("disabledDates", "2026-07-10"),
        ("disabledWeekdays", "Sat"),
        ("disabledMonths", "Dec"),
        ("disabledYears", 2025),
    ],
)
def test_disabled_lists_are_rejected_on_time_variant(key, entry):
    assert validate_date({key: [entry]}, "time") != []


def test_disabled_years_must_be_integers():
    assert validate_date({"disabledYears": ["2026"]}) != []


@pytest.mark.parametrize("variant", ["time", "datetime"])
@pytest.mark.parametrize(
    "windows",
    [
        [["12:00", "13:00"]],
        [["12:00:00", "13:00:30"], ["22:00", "24:00"]],
        [["2026-01-01T12:00:00", "2026-01-01 13:00:00"]],
        [["10:00", "23:59:59"]],
        [["18:00", "19:00"], ["10:00", "11:00"]],
    ],
)
def test_disabled_times_are_accepted(variant, windows):
    value = "2026-07-09T09:00:00" if variant == "datetime" else "09:00:00"
    assert validate_date({"disabledTimes": windows}, variant, value=value) == []


@pytest.mark.parametrize(
    "window",
    [
        ["13:00", "12:00"],
        ["12:00", "12:00"],
        ["24:00", "24:00"],
        ["24:00", "23:00"],
        ["12:00", "25:00"],
        ["12:00 PM", "13:00"],
        ["12", "13"],
        ["2026-07-09", "13:00"],
        ["12:00"],
        ["12:00", "13:00", "14:00"],
        [],
    ],
)
def test_malformed_disabled_times_are_rejected(window):
    log = validate_date({"disabledTimes": [window]}, "time")
    assert "error" in [e["level"] for e in log]


@pytest.mark.parametrize(
    "windows",
    [
        [["00:00", "24:00"]],
        [["00:00", "12:00"], ["12:00", "24:00:00"]],
        [["12:00", "24:00"], ["00:00", "13:00"]],
        [["00:00", "18:00"], ["06:00", "24:00"]],
    ],
)
def test_disabling_the_whole_day_is_an_error(windows):
    log = validate_date({"disabledTimes": windows}, "time")
    assert any(e["level"] == "error" and "whole day" in e["msg"] for e in log)


def test_windows_with_a_gap_do_not_disable_the_whole_day():
    windows = [["00:00", "12:00"], ["12:00:01", "24:00"]]
    assert validate_date({"disabledTimes": windows}, "time", value="12:00:00") == []


@pytest.mark.parametrize(
    "window, value, warns",
    [
        (["09:00", "10:00"], "09:00:00", True),
        (["09:00", "10:00"], "09:59:59", True),
        (["09:00", "10:00"], "10:00:00", False),
        (["09:00", "10:00"], "08:59:59", False),
        (["23:00", "24:00"], "23:59:59", True),
    ],
)
def test_value_inside_a_disabled_window_warns(window, value, warns):
    log = validate_date({"disabledTimes": [window]}, "time", value=value)
    assert [e["level"] for e in log] == (["warning"] if warns else [])


def test_datetime_value_inside_a_disabled_window_warns():
    log = validate_date({"disabledTimes": [["09:00", "10:00"]]}, "datetime")
    assert [e["level"] for e in log] == ["warning"]


def test_disabled_times_are_rejected_on_date_variant():
    assert validate_date({"disabledTimes": [["12:00", "13:00"]]}, "date") != []


def test_date_is_the_default_variant():
    assert validate_date({}, None) == []
    assert validate_date({}, None, value="2026-07-09T09:00:00") != []


@pytest.mark.parametrize(
    "prop",
    [
        {"views": ["year", "month", "day"], "defaultView": "month"},
        {"minDate": "2026-07-01", "maxDate": "2026-07-31"},
        {"disabledWeekdays": ["sat"], "disabledDates": ["2026-07-10"]},
    ],
)
def test_date_attrs_are_accepted_without_a_variant(prop):
    assert validate_date(prop, None) == []


@pytest.mark.parametrize(
    "prop",
    [
        {"views": ["hours"]},
        {"minTime": "08:00"},
        {"disabledTimes": [["12:00", "13:00"]]},
        {"hoursStep": 2},
    ],
)
def test_time_attrs_are_rejected_without_a_variant(prop):
    assert validate_date(prop, None) != []


@pytest.mark.parametrize("variant", [None, "date", "datetime"])
@pytest.mark.parametrize("order", ["mdy", "dmy", "ymd"])
def test_date_order_is_accepted(variant, order):
    assert validate_date({"dateOrder": order}, variant) == []


@pytest.mark.parametrize("order", ["MDY", "ydm", "iso", "", "YYYY-MM-DD"])
def test_unknown_date_order_is_rejected(order):
    assert validate_date({"dateOrder": order}, "date") != []


@pytest.mark.parametrize("variant", ["time", "datetime"])
@pytest.mark.parametrize("hour24", [True, False])
def test_hour24_is_accepted(variant, hour24):
    assert validate_date({"hour24": hour24}, variant) == []


def test_hour24_must_be_a_bool():
    assert validate_date({"hour24": "yes"}, "time") != []


@pytest.mark.parametrize(
    "variant, key, value",
    [("time", "dateOrder", "ymd"), ("date", "hour24", True), (None, "hour24", True)],
)
def test_display_attrs_are_rejected_on_variants_without_that_part(variant, key, value):
    assert validate_date({key: value}, variant) != []
