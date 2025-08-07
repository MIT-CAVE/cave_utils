from cave_utils import CustomCoordinateSystem

success = {
    "init": False,
    "serialize_coordinates": False,
    "serialize_nodes": False,
    "serialize_arcs": False,
    "bad_list_coordinates": False,
    "bad_dict_coordinates": False,
}

TOLERANCE = 0.1 # Expected coordinates are approximate

try:
    # Square (width = height)
    square_coordinate_system = CustomCoordinateSystem(1000, 1000)
    square_coordinates = [[0, 0], [200, 500], [500, 500], [750, 750]]
    expected_square_long_lat = [[-180, -85.05], [-108, 0], [0, 0], [90, 66.513]]
    actual_square_long_lat = square_coordinate_system.serialize_coordinates(square_coordinates)

    for index, actual_coordinate in enumerate(actual_square_long_lat):
        expected_coordinate = expected_square_long_lat[index]
        assert abs(actual_coordinate[0] - expected_coordinate[0]) < TOLERANCE
        assert abs(actual_coordinate[1] - expected_coordinate[1]) < TOLERANCE

    success["serialize_coordinates"] = True

    expected_square_location = {
        "latitude": [[-85.05], [0], [0], [66.513]],
        "longitude": [[-180], [-108], [0], [90]]
    }
    actual_square_location = square_coordinate_system.serialize_nodes(square_coordinates)

    for key in expected_square_location:
        assert key in actual_square_location
        for index, value in enumerate(expected_square_location[key]):
            assert abs(actual_square_location[key][index][0] - value[0]) < TOLERANCE

    # Landscape (width > height)
    landscape_coordinate_system = CustomCoordinateSystem(576, 360, 1000)
    landscape_coordinates = {
        "x": [0, 72, 288, 396, 432, 504, 252],
        "y": [180, 180, 180, 180, 216, 108, 36],
        "z": [0, 1000, 5, 0, 0, 390.5, 123]
    }
    expected_landscape_location = {
        "latitude": [[0], [0], [0], [0], [21.95], [-41], [-66.5]],
        "longitude": [[-180], [-135], [0], [67.5], [90], [135], [-22.5]],
        "altitude": [[0], [10000], [50], [0], [0], [3905], [1230]]
    }
    actual_landscape_location = landscape_coordinate_system.serialize_nodes(landscape_coordinates)

    for key in expected_landscape_location:
        assert key in actual_landscape_location
        for index, value in enumerate(expected_landscape_location[key]):
            assert abs(actual_landscape_location[key][index][0] - value[0]) < TOLERANCE
    
    success["serialize_nodes"] = True

    # Portrait (height > width)
    # TODO: change to arc example
    portrait_coordinate_system = CustomCoordinateSystem(100, 200)
    success["init"] = True

    portrait_coordinates = [[0, 0], [0, 100], [0, 125], [20, 100], [75, 125]]
    expected_portrait_long_lat = [[-90, -85.05], [-90, 0], [-90, 41], [-54, 0], [45, 41]]
    actual_portrait_long_lat = portrait_coordinate_system.serialize_coordinates(portrait_coordinates)

    for index, actual_coordinate in enumerate(actual_portrait_long_lat):
        expected_coordinate = expected_portrait_long_lat[index]
        assert abs(actual_coordinate[0] - expected_coordinate[0]) < TOLERANCE
        assert abs(actual_coordinate[1] - expected_coordinate[1]) < TOLERANCE


except Exception as e:
    pass
    # print(f"Error: {e}")
    # raise e

coordinate_system = CustomCoordinateSystem(1000, 1000, 1000)

def list_missing_altitude():
    coordinate_system.__validate_list_coordinates__([[0, 0, 0], [103.5, 99.1, 23], [76.55, 350, 35], [12.01, 12.01]])
def list_out_of_range():
    coordinate_system.__validate_list_coordinates__([[0, 0, -1], [1030.5, 99.1, 23]])
# TODO: add test with path/arc
bad_list_coordinates_tests = [list_missing_altitude, list_out_of_range]

for test in bad_list_coordinates_tests:
    try:
        test()
        break
    except ValueError as e:
        success["bad_list_coordinates"] = True

def dict_missing_altitude():
    coordinate_system.__validate_dict_coordinates__({
    "x": [0, 103.5, 76.55, 12.01],
    "y": [0, 99.1, 350, 12.01],
    "z": [0, 1, 0.2]
    })
def dict_missing_latitude():
    coordinate_system.__validate_dict_coordinates__({
    "x": [0, 103.5, 76.55, 12.01],
    "y": [0, 99.1, 12.01],
    "z": [0, 1, 0.2, 36]
    })
def dict_out_of_range():
    coordinate_system.__validate_list_coordinates__({
    "x": [0, 103.5, 76.55, 12.01],
    "y": [0, 99.1, 350, 12.01],
    "z": [0, 120, -0.2, 36]
    })
# TODO: add test with path/arc
bad_dict_coordinates_tests = [dict_missing_altitude, dict_missing_latitude, dict_out_of_range]

for test in bad_dict_coordinates_tests:
    try:
        test()
        break
    except ValueError as e:
        success["bad_dict_coordinates"] = True

if all(success.values()):
    print("Custom Coordinates Tests: Passed!")
else:
    print("Custom Coordinates Tests: Failed!")
    print(success)
