from cave_utils import Validator


def build_session_data(**slider_fields):
    slider = {
        "name": "Scaled Slider",
        "type": "num",
        "variant": "slider",
        "minValue": 1,
        "maxValue": 100,
        **slider_fields,
    }
    return {
        "settings": {
            "iconUrl": "https://react-icons.mitcave.com/5.4.0",
        },
        "appBar": {
            "data": {
                "examplePane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "data": {
                "examplePane": {
                    "name": "Example Props Pane",
                    "props": {"scaledSlider": slider},
                    "values": {"scaledSlider": 50},
                },
            },
        },
    }


def get_log(**slider_fields):
    return Validator(session_data=build_session_data(**slider_fields)).log.log


def assert_error(log, msg_fragment):
    errors = [i for i in log if i["level"] == "error"]
    assert any(
        msg_fragment in i["msg"] for i in errors
    ), f"Expected error containing {msg_fragment!r}, got: {log}"


def assert_warning(log, msg_fragment):
    warnings = [i for i in log if i["level"] == "warning"]
    assert any(
        msg_fragment in i["msg"] for i in warnings
    ), f"Expected warning containing {msg_fragment!r}, got: {log}"


def test_slider_without_scale():
    assert get_log() == []


def test_slider_scale_linear():
    assert get_log(scale="linear") == []


def test_slider_scale_log():
    # `base` is optional for a logarithmic scale (defaults to 10)
    assert get_log(scale="log") == []
    assert get_log(scale="log", scaleParams={"base": 2}) == []


def test_slider_scale_pow():
    assert get_log(scale="pow", scaleParams={"exponent": 2}) == []
    assert get_log(scale="pow", scaleParams={"exponent": 0.5}) == []


def test_slider_scale_exp():
    assert get_log(scale="exp", scaleParams={"base": 2}) == []
    assert get_log(scale="exp", scaleParams={"base": 0.5}) == []


def test_slider_scale_invalid_option():
    # `step` is a legend-only scale and not valid for sliders
    assert get_log(scale="step") != []


def test_slider_scale_pow_requires_exponent():
    assert_error(
        get_log(scale="pow"),
        "`exponent` must be specified for a power scale",
    )
    assert_error(
        get_log(scale="pow", scaleParams={}),
        "`exponent` must be specified for a power scale",
    )


def test_slider_scale_pow_invalid_exponent():
    msg = "`exponent` must be greater than 0 for a power scale"
    assert_error(get_log(scale="pow", scaleParams={"exponent": 0}), msg)
    assert_error(get_log(scale="pow", scaleParams={"exponent": -2}), msg)


def test_slider_scale_exp_requires_base():
    assert_error(
        get_log(scale="exp"),
        "`base` must be specified for an exponential scale",
    )
    assert_error(
        get_log(scale="exp", scaleParams={}),
        "`base` must be specified for an exponential scale",
    )


def test_slider_scale_invalid_base():
    msg = "`base` must be greater than 0 and not equal to 1"
    assert_error(get_log(scale="exp", scaleParams={"base": 1}), msg)
    assert_error(get_log(scale="exp", scaleParams={"base": 0}), msg)
    assert_error(get_log(scale="exp", scaleParams={"base": -2}), msg)
    assert_error(get_log(scale="log", scaleParams={"base": 1}), msg)


def test_slider_scale_log_allows_non_positive_bounds():
    # `log` only reshapes the thumb's position mapping (base^v), which is
    # defined for any real minValue/maxValue, so no positivity constraint applies
    assert get_log(scale="log", minValue=0, maxValue=100) == []
    assert get_log(scale="log", minValue=-10, maxValue=100) == []


def test_slider_scale_exp_requires_positive_bounds():
    min_msg = "`minValue` must be greater than 0 for an exponential scale"
    max_msg = "`maxValue` must be greater than 0 for an exponential scale"
    assert_error(get_log(scale="exp", scaleParams={"base": 2}, minValue=0), min_msg)
    assert_error(get_log(scale="exp", scaleParams={"base": 2}, minValue=-10), min_msg)
    assert_error(
        get_log(scale="exp", scaleParams={"base": 2}, minValue=-10, maxValue=0),
        max_msg,
    )


def test_slider_scale_irrelevant_params_warn():
    assert_warning(
        get_log(scale="pow", scaleParams={"exponent": 2, "base": 2}),
        "`base` has no effect on a `pow` scale",
    )
    assert_warning(
        get_log(scale="exp", scaleParams={"base": 2, "exponent": 2}),
        "`exponent` has no effect on a `exp` scale",
    )
    assert_warning(
        get_log(scaleParams={"base": 2}),
        "`base` has no effect on a `linear` scale",
    )
