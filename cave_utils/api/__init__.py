"""
This module is designed to help you validate your data against the CAVE API.

It also serves to document the API and provide a reference for the data structures.

.. include:: ./documentation.md
"""
from cave_utils.api.utils import *
from cave_utils.api.extraKwargs import extraKwargs
from cave_utils.api.settings import settings
from cave_utils.api.appBar import appBar
from cave_utils.api.panes import panes
from cave_utils.api.pages import pages
from cave_utils.api.maps import maps
from cave_utils.api.globalOutputs import globalOutputs


class Root(ApiValidator):
    """
    The root of the CAVE API data structure.

    This should include all of the data needed to build out your application.
    """

    @staticmethod
    def spec(
        settings: dict,
        appBar: dict,
        panes: dict = dict(),
        pages: dict = dict(),
        maps: dict = dict(),
        mapFeatures: dict = dict(),
        groupedOutputs: dict = dict(),
        globalOutputs: dict = dict(),
        extraKwargs: dict = dict(),
        **kwargs,
    ):
        """
        Required Arguments:

        - `settings:
            - Type: dict
            - What: General settings for your application.
            - Note: 'settings.iconUrl' is the only required field in `settings`
            - See: `settings.settings`
        - `appBar`:
            - Type: dict
            - What: Settings for the app bar.
            - Note: 'appBar.data' is required, and should have at least one item in it.
            - See: `appBar.appBar`

        Optional Arguments:

        - `panes`:
            - Type: dict
            - What: Configure panes for your application.
            - Default: `{}`
        - `pages`:
            - Type: dict
            - What: Configure pages for your application.
            - Default: `{}`
        - `maps`:
            - Type: dict
            - What: Configure map views and settings for your application.
            - Default: `{}`
        - `mapFeatures`:
            - Type: dict
            - What: Configure map features (interactive items on the map) for your application.
            - Default: `{}`
        - `groupedOutputs`:
            - Type: dict
            - What: Configure data that can be sliced and diced for charts and tables based on arbitrary groups.
            - Default: `{}`
        - `globalOutputs`:
            - Type: dict
            - What: Configure data that is general to the entire application and can be compared across sessions.
            - Default: `{}`
        - `extraKwargs`:
            - Type: dict
            - What: Special arguments to be passed to the server.
            - Default: `{}`

        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        # Validate Kwargs
        if "extraKwargs" in self.data:
            extraKwargs(
                data=self.data.get("extraKwargs", {}),
                log=self.log,
                prepend_path=["kwargs"],
                **kwargs,
            )
        # Validate Settings
        settings(
            data=self.data.get("settings", {}),
            log=self.log,
            prepend_path=["settings"],
            root_data=self.data,
            **kwargs,
        )
        # Validate panes
        panes_data = self.data.get("panes")
        pane_validPaneIds = []
        if panes_data is not None:
            panes(data=panes_data, log=self.log, prepend_path=["panes"], **kwargs)
            pane_validPaneIds = list(panes_data.get("data", {}).keys())
        # Validate mapFeatures
        # TODO
        # Validate maps
        maps_data = self.data.get("maps")
        maps_validMapIds = []
        if maps_data is not None:
            # TODO: Validate mapFeatures
            maps(data=maps_data, log=self.log, prepend_path=["maps"], **kwargs)
            maps_validMapIds = list(maps_data.get("data", {}).keys())
        # Validate globalOutputs
        globalOutputs_data = self.data.get("globalOutputs", None)
        globalOuputs_validPropIds = []
        if globalOutputs_data is not None:
            globalOutputs(
                data=globalOutputs_data,
                log=self.log,
                prepend_path=["globalOutputs"],
                **kwargs,
            )
            globalOuputs_validPropIds = list(globalOutputs_data.get("values", {}).keys())

        # Validate groupedOutputs
        # TODO
        # Validate pages
        pages_data = self.data.get("pages")
        page_validPageIds = []
        if pages_data is not None:
            pages(
                data=pages_data, 
                log=self.log, 
                prepend_path=["pages"],
                # Special Kwargs:
                globalOuputs_validPropIds=globalOuputs_validPropIds,
                maps_validMapIds=maps_validMapIds,
                **kwargs
            )
            page_validPageIds = list(pages_data.get("data", {}).keys())
        # Validate appBar
        appBar_data = self.data.get("appBar")
        if appBar_data is not None:
            appBar(
                data=appBar_data, 
                log=self.log, 
                prepend_path=["appBar"], 
                # Special kwargs to validate panes and pages are valid:
                page_validPageIds=page_validPageIds,
                pane_validPaneIds=pane_validPaneIds,
                **kwargs
            )


class Validator:
    def __init__(self, session_data, ignore_keys: list = list(), **kwargs):
        """
        Util to validate your session_data against the API spec.

        Required Arguments:

        - `session_data`:
            - Type: dict
            - What: The data to validate.
            - Note: This should be the data you are sending to the server.

        Optional Arguments:

        - `ignore_keys`:
            - Type: list
            - What: Keys to ignore when validating.
            - Note: Any keys specified here will be not be validated if encountered in the data at any level.
        """
        self.session_data = session_data
        self.log = LogObject()
        assert isinstance(
            ignore_keys,
            (
                list,
                set,
            ),
        ), "`ignore_keys` must be a list of strings or set of strings"
        Root(data=self.session_data, log=self.log, prepend_path=[], ignore_keys=set(ignore_keys))
