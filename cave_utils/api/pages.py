"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
import type_enforced

@type_enforced.Enforcer
class pages_data_star_pageLayout(ApiValidator):
    """
    ## Api Path: pages.data.*.pageLayout
    """
    @staticmethod
    def spec(
        type: str = 'groupedOutput', 
        variant: str = 'bar', 
        mapId: [str, None] = None,
        groupingId: [list, None] = None,
        sessions: [list, None] = None,
        globalOutput: [list, None] = None,
        groupingLevel:[list, None] = None,
        lockedLayout: bool=False,
        statAggregation: str = "sum",
        groupedOutputDataId: [str, None] = None,
        statId: [str, None] = None,
        showToolbar: bool = True,
        maximized: bool = False,
        **kwargs):
        """
        Optional Arguments:

        - `type`:
            - Type: str
            - What: The type of the page layout.
            - Default: `'groupedOutputs'`
            - Accepted Values: `['groupedOutput', 'globalOutput', 'map']`
        - `variant`:
            - Type: str
            - What: The variant of the page layout.
            - Default: `'bar'`
            - Accepted Values: 
                - TODO: Update this list
                - Type: `groupedOutput`
                    - `['bar', 'line', 'table', 'box_plot', 'cumulative_line']`
                - Type: `globalOutput`
                    - `['bar', 'line', 'table']`
        - `mapId`:
            - Type: str
            - What: The id of the map to use.
            - Default: `None`
        - `groupingId`:
            - Type: list
            - What: The ids of the grouping to use.
            - Default: `None`
        - `sessions`:
            - Type: list
            - What: The ids of the sessions to use.
            - Default: `None`
        - `globalOutput`:
            - Type: list
            - What: The ids of the global outputs to use.
            - Default: `None`
        - `groupingLevel`:
            - Type: list
            - What: The ids of the grouping levels to use.
            - Default: `None`
        - `lockedLayout`:
            - Type: bool
            - What: Whether or not the layout should be locked.
            - Default: `False`
        - `statAggregation`:
            - Type: str
            - What: The stat aggregation to use.
            - Default: `'sum'`
            - Accepted Values: `['sum', 'mean', 'median', 'min', 'max', 'count']`
        - `groupedOutputDataId`:
            - Type: str
            - What: The id of the grouped output data to use.
            - Default: `None`
        - `statId`:
            - Type: str
            - What: The id of the stat to use.
            - Default: `None`
        - `showToolbar`:
            - Type: bool
            - What: Whether or not the toolbar should be shown.
            - Default: `True`
        - `maximized`:
            - Type: bool
            - What: Whether or not the layout should be maximized.
            - Default: `False`
        """
        if type == 'globalOutput':
            variant_options = ['bar', 'line', 'table']
        elif type == 'groupedOutput':
            variant_options = ['bar', 'line', 'table', 'box_plot', 'cumulative_line']
        else:
            variant_options = []
        return {"kwargs": kwargs, "accepted_values": {
            # TODO: Validate these are correct
            'type': ['groupedOutput', 'globalOutput', 'map'],
            'variant': variant_options,
            'statAggregation': ['sum', 'mean', 'median', 'min', 'max', 'count'],
        }}

    def __extend_spec__(self, **kwargs):
        globalOutput = self.data.get("globalOutput")
        if globalOutput is not None:
            self.__check_subset_valid__(
                subset=globalOutput, valid_values=kwargs.get("globalOuputs_validPropIds", []), prepend_path=["globalOutput"]
            )
        mapId = self.data.get("mapId")
        if mapId is not None:
            self.__check_subset_valid__(
                subset=[mapId], valid_values=kwargs.get("maps_validMapIds", []), prepend_path=["mapId"]
            )
        # TODO: Validate groupingId, groupingLevel, statId, groupedOutputDataId
        pass

@type_enforced.Enforcer
class pages_data_star(ApiValidator):
    """
    ## Api Path: pages.data.*
    """

    @staticmethod
    def spec(pageLayout: list, lockedLayout: bool = False, **kwargs):
        """
        Required Arguments:

        - `pageLayout`:
            - Type: list
            - What: The layout of the page.
            - See: `cave_utils.api.pages.pages_data_star_pageLayout`
        - `lockedLayout`:
            - Type: bool
            - What: Whether or not the layout should be locked.
            - Default: `False`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        for idx, pageLayout in enumerate(self.data.get("pageLayout", [])):
            pages_data_star_pageLayout(
                data=pageLayout,
                log=self.log,
                prepend_path=["pageLayout", idx],
                **kwargs,
            )


@type_enforced.Enforcer
class pages(ApiValidator):
    """
    ## Api Path: pages
    """
    @staticmethod
    def spec(currentPage: [str, None] = None, data: dict = dict(), **kwargs):
        """
        Optional Arguments:
        - `current_page`:
            - Type: str
            - What: The id of the current page that is being rendered.
            - Default: `None`
        - `data`:
            - Type: dict
            - What: The data to pass to `pages.data.*`.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=pages_data_star, **kwargs
        )
        currentPage = self.data.get("currentPage")
        if isinstance(currentPage, str):
            self.__check_subset_valid__(
                subset=[currentPage], valid_values=list(data.keys()), prepend_path=["currentPage"]
            )
