from cave_utils.api_spec.utils import *

class appBar(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "data": dict,
            "allowModification": bool,
            "sendToApi": bool,
            "sendToClient": bool,
        }
        self.accepted_values = {}
        self.required_fields = []
        self.optional_fields = ["allowModification", "sendToApi", "sendToClient", "data"]

    def __additional_validations__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=appBar_data, **kwargs
        )


class appBar_data(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "icon": str,
            "type": str,
            "bar": str,
            "variant": str,
            "color": str,
            "apiCommand": str,
            "apiCommandKeys": list,
        }
        self.accepted_values = {
            "type": ["session", "settings", "button", "pane", "page"],
            "variant": ["modal", "wall"] if self.data.get("type") == "pane" else [],
            "bar": ["upperLeft", "lowerLeft", "upperRight", "lowerRight"],
        }
        self.required_fields = ["icon", "type", "bar"]
        self.optional_fields = ["variant", "color", "apiCommand", "apiCommandKeys"]

    def __additional_validations__(self, **kwargs):
        color = self.data.get("color")
        if color:
            self.check_rgba_string_valid(
                rgba_string=color,
                prepend_path=["color"]
            )