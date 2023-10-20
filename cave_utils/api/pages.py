"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import *
import type_enforced


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
            - See: `cave_utils.api.utils.PageLayoutValidator`
        - `lockedLayout`:
            - Type: bool
            - What: Whether or not the layout should be locked.
            - Default: `False`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        # TODO: Validate Page Layout
        pass


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
