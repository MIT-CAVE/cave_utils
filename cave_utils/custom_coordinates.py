import math
import type_enforced

class CustomCoordinateSystem():
    @type_enforced.Enforcer
    def __init__(self, width: float | int, height: float | int):
        """
        Creates a custom Cartesian coordinate system with the origin (0, 0) located at the bottom-left
        of the map and x and y increasing in value whilst moving right and up, respectively.

        Arguments:

        * **`width`**: `[float | int]` &rarr; The maximum x value of this coordinate system.
        * **`height`**: `[float | int]` &rarr; The maximum y value of this coordinate system.

        Returns:

        * `[None]`
        """
        self.width = width
        self.height = height
        self.radius = max(width, height) / (2 * math.pi)
        self.margin = abs(width - height) / 2

    def convert_to_long_lat(self, coordinates: list[list[float | int]]):
        """
        Converts (x, y) coordinates using this coordinate system to a longitude-latitude system.
        Formula adapted from: https://en.wikipedia.org/wiki/Mercator_projection#Derivation

        Arguments:

        * **`coordinates`**: `list[list[float | int]]` &rarr; The coordinates to be converted in this coordinate system in the format `[[x1,y1],[x2,y2],...]`.
            * ** Example **: `[[0,0],[103.5,99.1],[76.55,350],[12.01,12.01]]`

        Returns:

        * `list[list[float | int]]` &rarr; The converted coordinates in the format [[long1,lat1],[long2,lat2],...].
        """
        long_lat_coordinates = []
        for coordinate in coordinates:
            x = coordinate[0]
            y = coordinate[1] - self.height / 2

            if self.height > self.width:
                x += self.margin

            longitude = (x / self.radius) * (180 / math.pi)
            latitude = (360 / math.pi) * (math.atan(math.exp(y / self.radius)) - math.pi / 4)

            # Y values close to 0 will not display on map 
            if latitude < -85.05 and coordinate[1] >= 0:
                latitude = -85.05
            long_lat_coordinates.append([longitude - 180, latitude])

        return long_lat_coordinates
