from shapely.geometry import Polygon, mapping
from pyproj import Geod

geod = Geod(ellps="WGS84")


class Region:
    def __init__(self, poly):
        coords = poly["geometry"]["coordinates"]

        shell, holes = None, None

        if len(coords) == 1:
            shell = coords[0]
        else:
            shell = coords[0]
            holes = coords[1]

            if isinstance(holes[0][0], float):
                holes = [holes]

            if isinstance(shell[0], list):
                shell = shell[0]

        self.poly = Polygon(shell, holes=holes)

    def get_area(self) -> float:
        return abs(geod.geometry_area_perimeter(self.poly)[0])

    @property
    def mapping(self):
        return mapping(self.poly)
