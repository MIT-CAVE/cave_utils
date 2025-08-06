import math
from cave_utils import CustomCoordinateSystem

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

    # Landscape (width > height)
    landscape_coordinate_system = CustomCoordinateSystem(576, 360)
    landscape_coordinates =  [
        [0, 180],
        [72, 180],
        [288, 180],
        [396, 180],
        [432, 216],
        [504, 108],
        [252, 36]
        ]
    expected_landscape_long_lat = [
        [-180, 0],
        [-135, 0],
        [0, 0],
        [67.5, 0],
        [90, 21.95],
        [135, -41],
        [-22.5, -66.5]
        ]
    actual_landscape_long_lat = landscape_coordinate_system.serialize_coordinates(landscape_coordinates)

    for index, actual_coordinate in enumerate(actual_landscape_long_lat):
        expected_coordinate = expected_landscape_long_lat[index]
        assert abs(actual_coordinate[0] - expected_coordinate[0]) < TOLERANCE
        assert abs(actual_coordinate[1] - expected_coordinate[1]) < TOLERANCE

    # Portrait (height > width)
    portrait_coordinate_system = CustomCoordinateSystem(100, 200)
    portrait_coordinates = [[0, 0], [0, 100], [0, 125], [20, 100], [75, 125]]
    expected_portrait_long_lat = [[-90, -85.05], [-90, 0], [-90, 41], [-54, 0], [45, 41]]
    actual_portrait_long_lat = portrait_coordinate_system.serialize_coordinates(portrait_coordinates)

    for index, actual_coordinate in enumerate(actual_portrait_long_lat):
        expected_coordinate = expected_portrait_long_lat[index]
        assert abs(actual_coordinate[0] - expected_coordinate[0]) < TOLERANCE
        assert abs(actual_coordinate[1] - expected_coordinate[1]) < TOLERANCE

    print(f"Custom Coordinates Tests: Passed!")

except Exception as e:
    print(f"Custom Coordinates Tests: Failed!")
    print(f"Error: {e}")
    raise e
