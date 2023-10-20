"""
Build out an app bar with buttons to launch pages, launch maps and trigger api commands.
"""
from cave_utils.api.utils import *
import type_enforced


@type_enforced.Enforcer
class maps_data_star(ApiValidator):
    """
    ## Api Path: maps.data.*
    """

    @staticmethod
    def spec(
        name: str,
        currentStyle: [str, None] = None,
        currentProjection: [str, None] = None,
        defaultViewport: [dict, None] = None,
        optionalViewports: [dict, None] = None,
        legendGroups: [dict, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the map.
        - `currentStyle`:
            - Type: str
            - What: The id of the style to use when the map is first loaded.
            - Default: `None`
        - `currentProjection`:
            - Type: str
            - What: The id of the projection to use when the map is first loaded.
            - Default: `None`
            - Valid Values: `mercator`, `globe`
        - `defaultViewport`:
            - Type: dict
            - What: The default viewport to use.
            - Default: `None`
            - Note: `defaultViewport` is not validated except that it should be a dict.
            - See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setviewport
        - `optionalViewports`:
            - Type: dict
            - What: The optional viewports that can be selected by the end user.
            - Note: `optionalViewports` is not validated except that it should be a dict.
            - See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setviewport
        - `legendGroups`:
            - Type: dict
            - What: The legend groups to show in the map selection menu.
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        # TODO: Validate Here
        pass


@type_enforced.Enforcer
class maps_additionalMapStyles_star(ApiValidator):
    """
    ## Api Path: maps.additionalMapStyles.*
    """

    @staticmethod
    def spec(name: str, icon: str, spec: [dict, str], fog: [dict, None] = None, **kwargs):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the style.
        - `icon`:
            - Type: str
            - What: The icon to show in the map selection menu.
        - `spec`:
            - Type: dict | str
            - What: The spec to generate the map
            - See: Mapbox: https://docs.mapbox.com/api/maps/styles/
            - See: Carto: https://github.com/CartoDB/basemap-styles/blob/master/docs/basemap_styles.json
            - See: Raster: https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
            - Note: `spec` can be a dict or a string. If it is a string, it will be treated as a url to a json file.
            - Note: `spec` is not validated except that it should be a dict or a string.

        Optional Arguments:

        - `fog`:
            - Type: dict
            - What: The fog to show in the map selection menu.
            - Note: Fog is not validated except that it should be a dict.
            - See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setfog
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        pass
        # TODO: Validate icon
        # TODO: Possibly validate spec and fog


@type_enforced.Enforcer
class maps(ApiValidator):
    """
    ## Api Path: maps
    """

    @staticmethod
    def spec(additionalMapStyles: dict = dict(), data: dict = dict(), **kwargs):
        """
        Optional Arguments:

        - `data`:
            - Type: dict
            - What: The data to pass to `maps.data.*`.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=maps_data_star, **kwargs
        )
        CustomKeyValidator(
            data=self.data.get("additionalMapStyles", {}),
            log=self.log,
            prepend_path=["additionalMapStyles"],
            validator=maps_additionalMapStyles_star,
            **kwargs,
        )
