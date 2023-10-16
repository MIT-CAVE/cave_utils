from cave_utils.api_spec.utils import *


class settings(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "data": dict,
            "allowModification": bool,
            "sendToApi": bool,
            "sendToClient": bool,
        }

        self.accepted_values = {}

        self.required_fields = ["data"]

        self.optional_fields = ["allowModification", "sendToApi", "sendToClient"]

    def __additional_validations__(self, **kwargs):
        settings_data(
            data=self.data.get("data", {}), log=self.log, prepend_path=["data"], **kwargs
        )


class settings_data(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "iconUrl": str,
            "demo": dict,
            "sync": dict,
            "time": dict,
            "defaults": dict,
            "debug": bool,
        }
        self.accepted_values = {}
        self.required_fields = ["iconUrl"]
        self.optional_fields = ["demo", "sync", "time", "defaults", "debug"]

    def __additional_validations__(self, **kwargs):
        self.check_url_valid(
            url=self.data.get("iconUrl"),
        )
        CustomKeyValidator(
            data=self.data.get("sync", {}),
            log=self.log,
            prepend_path=["sync"],
            validator=settings_data_sync,
            **kwargs,
        )
        CustomKeyValidator(
            data=self.data.get("demo", {}),
            log=self.log,
            prepend_path=["demo"],
            validator=settings_data_demo,
            **kwargs,
        )
        if self.data.get("time"):
            settings_data_time(
                data=self.data.get("time", {}),
                log=self.log,
                prepend_path=["time"],
                **kwargs,
            )
        settings_data_defaults(
            data=self.data.get("defaults", {}),
            log=self.log,
            prepend_path=["defaults"],
            **kwargs,
        )


class settings_data_sync(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "name": str,
            "showToggle": bool,
            "value": bool,
            "data": dict,
        }
        self.accepted_values = {}
        self.required_fields = ["name", "showToggle", "value", "data"]
        self.optional_fields = []

    # def __additional_validations__(self, **kwargs):
    #     root_data = kwargs.get("root_data", {})
    #     for key, path in self.data.get("data", {}).items():
    #         if not pamda.hasPath(path, root_data):
    #             self.warn(f"Path {path} does not exist.", prepend_path=["data", key])


class settings_data_demo(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "scrollSpeed": (int, float),
            "displayTime": int,
        }
        self.accepted_values = {}
        self.required_fields = []
        self.optional_fields = ["scrollSpeed", "displayTime"]


class settings_data_time(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "timeLength": int,
            "timeUnits": str,
        }
        self.accepted_values = {}
        self.required_fields = ["timeLength", "timeUnits"]
        self.optional_fields = []


class settings_data_defaults(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "precision": int,
            "trailingZeros": bool,
            "unitPlacement": str,
            "showToolbar": bool,
        }
        self.accepted_values = {
            # TODO: "unitPlacement": [],
        }
        self.required_fields = []
        self.optional_fields = ["precision", "trailingZeros", "unitPlacement", "showToolbar"]
