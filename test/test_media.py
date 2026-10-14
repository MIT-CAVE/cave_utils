"""
Test-only coverage for `media` props: variants, `scaleMode`, `fullWidth` precedence, and
url/variant mismatch warnings.
"""

import pytest
from cave_utils import Validator

SETTINGS = {"iconUrl": "https://react-icons.mitcave.com/5.4.0"}
IMAGE = "https://example.com/picture.png"
VIDEO = "https://www.youtube.com/embed/6q5R1TDmKnU"
AUDIO = "https://example.com/clip.mp3"


def validate_media(prop, value):
    session_data = {
        "settings": SETTINGS,
        "globalOutputs": {
            "props": {"m": {"name": "M", "type": "media", **prop}},
            "values": {"m": value},
        },
    }
    return Validator(session_data, ignore_keys=["meta"]).log.log


def messages(log, level):
    return [entry["msg"] for entry in log if entry.get("level") == level]


@pytest.mark.parametrize(
    "variant,value",
    [("picture", IMAGE), ("video", VIDEO), ("audio", AUDIO)],
)
def test_variants_are_valid(variant, value):
    assert validate_media({"variant": variant}, value) == []


@pytest.mark.parametrize("variant", ["picture", "video"])
@pytest.mark.parametrize("scale_mode", ["fitWidth", "fitHeight", "fitContainer"])
def test_scale_mode_accepted_for_picture_and_video(variant, scale_mode):
    value = {"picture": IMAGE, "video": VIDEO}[variant]
    assert validate_media({"variant": variant, "scaleMode": scale_mode}, value) == []


def test_scale_mode_not_supported_for_audio():
    log = validate_media({"variant": "audio", "scaleMode": "fitWidth"}, AUDIO)
    assert len(log) > 0


def test_full_width_supported_for_audio():
    assert validate_media({"variant": "audio", "fullWidth": True}, AUDIO) == []


def test_scale_mode_rejected_for_unrelated_type():
    session_data = {
        "settings": SETTINGS,
        "globalOutputs": {
            "props": {"t": {"name": "T", "type": "text", "scaleMode": "fitWidth"}},
            "values": {"t": "text"},
        },
    }
    log = Validator(session_data, ignore_keys=["meta"]).log.log
    assert len(log) > 0


def test_full_width_with_scale_mode_warns():
    log = validate_media(
        {"variant": "picture", "fullWidth": True, "scaleMode": "fitWidth"}, IMAGE
    )
    assert len(log) == 1
    assert log[0]["level"] == "warning"
    assert "takes precedence" in log[0]["msg"]


def test_full_width_alone_does_not_warn():
    assert validate_media({"variant": "picture", "fullWidth": True}, IMAGE) == []


def test_full_width_false_with_scale_mode_does_not_warn():
    log = validate_media(
        {"variant": "picture", "fullWidth": False, "scaleMode": "fitHeight"}, IMAGE
    )
    assert log == []


@pytest.mark.parametrize(
    "variant,value",
    [
        ("picture", VIDEO),
        ("picture", "https://vimeo.com/123456"),
        ("picture", "https://example.com/clip.mp4"),
        ("picture", AUDIO),
        ("video", IMAGE),
        ("video", AUDIO),
        ("audio", IMAGE),
        ("audio", "https://example.com/clip.mp4"),
        ("audio", VIDEO),
    ],
)
def test_clear_url_variant_mismatch_warns(variant, value):
    log = validate_media({"variant": variant}, value)
    assert len(log) == 1
    assert log[0]["level"] == "warning"
    assert "variant" in log[0]["msg"]


@pytest.mark.parametrize(
    "variant,value",
    [
        # Unknown hosts and extensionless urls are never flagged
        ("picture", "https://cdn.example.com/asset/12345"),
        ("video", "https://player.example.com/embed/12345"),
        ("audio", "https://cdn.example.com/stream?token=abc"),
        # Ambiguous containers are never flagged
        ("audio", "https://example.com/clip.ogg"),
        ("audio", "https://example.com/clip.webm"),
        ("video", "https://example.com/clip.webm"),
        # Query strings do not affect the extension
        ("picture", "https://example.com/picture.png?w=400"),
        ("audio", "https://example.com/clip.mp3?download=1"),
    ],
)
def test_ambiguous_or_unknown_urls_are_accepted(variant, value):
    assert validate_media({"variant": variant}, value) == []
