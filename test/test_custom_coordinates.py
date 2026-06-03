import pytest
from cave_utils import CustomCoordinateSystem

TOLERANCE = 0.1


def test_custom_coordinates():
    square_coordinate_system = CustomCoordinateSystem(1000, 1000)
    square_coordinates = [[0, 0], [200, 500], [500, 500], [750, 750]]
    expected_square_long_lat = [[-180, -85.05], [-108, 0], [0, 0], [90, 66.513]]
    actual_square_long_lat = square_coordinate_system.serialize_coordinates(square_coordinates)
    for index, actual_coordinate in enumerate(actual_square_long_lat):
        expected_coordinate = expected_square_long_lat[index]
        assert abs(actual_coordinate[0] - expected_coordinate[0]) < TOLERANCE
        assert abs(actual_coordinate[1] - expected_coordinate[1]) < TOLERANCE

    expected_square_location = {
        "latitude": [[-85.05], [0], [0], [66.513]],
        "longitude": [[-180], [-108], [0], [90]],
    }
    actual_square_location = square_coordinate_system.serialize_nodes(square_coordinates)
    for key in expected_square_location:
        assert key in actual_square_location
        for index, value in enumerate(expected_square_location[key]):
            assert abs(actual_square_location[key][index][0] - value[0]) < TOLERANCE

    landscape_coordinate_system = CustomCoordinateSystem(576, 360, 1000)
    landscape_coordinates = {
        "x": [0, 72, 288, 396, 432, 504, 252],
        "y": [180, 180, 180, 180, 216, 108, 36],
        "z": [0, 1000, 5, 0, 0, 390.5, 123],
    }
    expected_landscape_location = {
        "latitude": [[0], [0], [0], [0], [21.95], [-41], [-66.5]],
        "longitude": [[-180], [-135], [0], [67.5], [90], [135], [-22.5]],
        "altitude": [[0], [10000], [50], [0], [0], [3905], [1230]],
    }
    actual_landscape_location = landscape_coordinate_system.serialize_nodes(landscape_coordinates)
    for key in expected_landscape_location:
        assert key in actual_landscape_location
        for index, value in enumerate(expected_landscape_location[key]):
            assert abs(actual_landscape_location[key][index][0] - value[0]) < TOLERANCE

    portrait_coordinate_system = CustomCoordinateSystem(100, 200, 200)

    portrait_coordinates_list = [
        [[0, 0, 0], [0, 100, 0]],
        [[0, 125, 0], [20, 100, 100], [75, 125, 150]],
    ]
    portrait_coordinates_dict = [
        {"x": [0, 0], "y": [0, 100], "z": [0, 0]},
        {"x": [0, 20, 75], "y": [125, 100, 125], "z": [0, 100, 150]},
    ]
    expected_portrait_location = {
        "path": [[[-90, -85.05, 0], [-90, 0, 0]], [[-90, 41, 0], [-54, 0, 5000], [45, 41, 7500]]]
    }
    actual_portrait_location_list = portrait_coordinate_system.serialize_arcs(
        portrait_coordinates_list
    )
    actual_portrait_location_dict = portrait_coordinate_system.serialize_arcs(
        portrait_coordinates_dict
    )
    assert "path" in actual_portrait_location_list and "path" in actual_portrait_location_dict
    assert (
        len(expected_portrait_location["path"])
        == len(actual_portrait_location_list["path"])
        == len(actual_portrait_location_dict["path"])
    )
    for arc_index, arc in enumerate(expected_portrait_location["path"]):
        assert (
            len(expected_portrait_location["path"][arc_index])
            == len(actual_portrait_location_list["path"][arc_index])
            == len(actual_portrait_location_dict["path"][arc_index])
        )
        for coordinate_index, coordinate in enumerate(arc):
            actual_coordinate_list = actual_portrait_location_list["path"][arc_index][
                coordinate_index
            ]
            actual_coordinate_dict = actual_portrait_location_dict["path"][arc_index][
                coordinate_index
            ]
            for index, expected_value in enumerate(coordinate):
                assert abs(actual_coordinate_list[index] - expected_value) < TOLERANCE
                assert abs(actual_coordinate_dict[index] - expected_value) < TOLERANCE


def test_bad_init():
    with pytest.raises(ValueError):
        CustomCoordinateSystem(0, 100)
    with pytest.raises(ValueError):
        CustomCoordinateSystem(250.05, -10)
    with pytest.raises(ValueError):
        CustomCoordinateSystem(100, 1, 0)
    with pytest.raises(ValueError):
        CustomCoordinateSystem(250, 0, -5)


def test_bad_list_coordinates():
    coordinate_system = CustomCoordinateSystem(100, 1000, 1000)
    with pytest.raises(ValueError):
        coordinate_system.__validate_list_coordinates__(
            [[0, 0, 0], [93.5, 99.1, 23], [76.55, 350, 35], [12.01, 12.01]]
        )
    with pytest.raises(ValueError):
        coordinate_system.__validate_list_coordinates__([[0, 0, -1], [930.5, 99.1, 23]])
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [[[0, 0, 0], [93.5, 99.1, 23]], [[76.55, 350], [12.01, 12.01, 12.01]]]
        )
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [[[0, 0, 0], [93.5, 99.1, 23]], [[76.55, 350], [12.01, 12.01]]]
        )
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [[[0, 0, 0], [93.5, 99.1, 200]], [[76.55, 1000.1, 30], [12.01, 12.01, 30]]]
        )


def test_bad_dict_coordinates():
    coordinate_system = CustomCoordinateSystem(100, 1000, 1000)
    with pytest.raises(ValueError):
        coordinate_system.__validate_dict_coordinates__(
            {"x": [0, 103.5, 76.55, 12.01], "y": [0, 99.1, 350, 12.01], "z": [0, 1, 0.2]}
        )
    with pytest.raises(ValueError):
        coordinate_system.__validate_dict_coordinates__(
            {"x": [0, 103.5, 76.55, 12.01], "y": [0, 99.1, 12.01], "z": [0, 1, 0.2, 36]}
        )
    with pytest.raises(ValueError):
        coordinate_system.__validate_dict_coordinates__(
            {"x": [103.5, 76.55, 12.01], "y": [0, 99.1, 350, 12.01], "z": [0, 1, 0.2, 36]}
        )
    with pytest.raises(ValueError):
        coordinate_system.__validate_dict_coordinates__(
            {"x": [0, 103.5, 76.55, 12.01], "y": [0, 99.1, 350, 12.01], "z": [0, 120, -0.2, 36]}
        )
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [
                {"x": [0, 103.5], "y": [0, 99.1], "z": [0, 23]},
                {"x": [76.55, 12.01], "y": [350, 12.01], "z": [12.01]},
            ]
        )
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [
                {"x": [0, 103.5], "y": [0, 99.1], "z": [0, 23]},
                {"x": [76.55, 12.01], "y": [350, 12.01]},
            ]
        )
    with pytest.raises(ValueError):
        coordinate_system.serialize_arcs(
            [
                {"x": [0, 103.5], "y": [0, 99.1], "z": [0, 200]},
                {"x": [76.55, 12.01], "y": [1000.1, 12.01], "z": [30, 30]},
            ]
        )
