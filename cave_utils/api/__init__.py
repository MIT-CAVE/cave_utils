"""
This module is designed to help you validate your data against the CAVE API.

It also serves to document the API and provide a reference for the data structures.

.. include:: ./documentation.md
"""
from cave_utils.api.utils import *
from cave_utils.api.kwargs import kwargs as KwargsValidator
from cave_utils.api.settings import settings
from cave_utils.api.appBar import appBar

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
        kwargs: dict = dict(),
        **otherKwargs
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
        - `kwargs`:
            - Type: dict
            - What: Special arguments to be passed to the server.
            - Default: `{}`

        """
        return otherKwargs

    def __populate_data__(self, **otherKwargs):
        self.field_types = {
            "settings": dict,
            "appBar": dict,
            "panes": dict,
            "pages": dict,
            "maps": dict,
            "mapFeatures": dict,
            "groupedOutputs": dict,
            "globalOutputs": dict,
            "kwargs": dict,
        }
        self.required_fields = ['settings', 'appBar']
        self.optional_fields = ['panes', 'pages', 'maps', 'mapFeatures', 'groupedOutputs', 'globalOutputs', 'kwargs']
        self.accepted_values = {}

    def __additional_validations__(self, **kwargs):
        # Validate Kwargs
        if "kwargs" in self.data:
            KwargsValidator(
                data=self.data.get("kwargs", {}), log=self.log, prepend_path=["kwargs"], **kwargs
            )
        # Validate Settings
        settings(
            data=self.data.get("settings", {}),
            log=self.log,
            prepend_path=["settings"],
            root_data=self.data,
            **kwargs,
        )
        # Validate appBar
        appBar(
            data=self.data.get("appBar", {}), 
            log=self.log, 
            prepend_path=["appBar"], 
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
        Root(
            data=self.session_data, log=self.log, prepend_path=[], ignore_keys=set(ignore_keys)
        )
