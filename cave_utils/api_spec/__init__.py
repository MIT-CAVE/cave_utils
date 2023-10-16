from cave_utils.api_spec.utils import *
from cave_utils.api_spec.kwargs import kwargs as KwargsValidator
from cave_utils.api_spec.settings import settings
from cave_utils.api_spec.appBar import appBar
from cave_utils.api_spec.pages import pages

class Root(ApiValidator):
    def __populate_data__(self, **kwargs):
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
    def __init__(self, session_data, ignore_keys: list = [], **kwargs):
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
