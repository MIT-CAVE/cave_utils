from cave_utils.api_spec.utils import *


class pages(ApiValidator):
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
        CustomKeyValidator(
            data=self.data.get("data", {}),
            log=self.log,
            prepend_path=["data"],
            validator=pages_data,
            **kwargs,
        )


class pages_data(ApiValidator):
    def __populate_data__(self, **kwargs):
        variant = self.data.get("variant")

        self.field_types = {
            "variant": str,
            "name": str,
            "props": dict,
            "layout": dict,
            "data": dict,
            "teamSyncCommand": str,
            "teamSyncCommandKeys": list,
        }

        self.accepted_values = {
            "variant": ["session", "appSettings", "options", "context", "filter"],
        }

        self.required_fields = ["name"]

        self.optional_fields = ["variant"]

        if variant == "options":
            self.required_fields += ["props"]
            self.optional_fields += ["layout", "teamSyncCommand", "teamSyncCommandKeys"]
        if variant == "context":
            self.required_fields += ["props"]
            self.optional_fields += ["data", "teamSyncCommand", "teamSyncCommandKeys"]

    def __additional_validations__(self, **kwargs):
        variant = self.data.get("variant")
        props_data = self.data.get("props", {})
        if variant == "options":
            CustomKeyValidator(
                data=props_data,
                log=self.log,
                prepend_path=["props"],
                validator=PropValidator,
                **kwargs,
            )
            LayoutValidator(
                data=self.data.get("layout", {}),
                log=self.log,
                prepend_path=["layout"],
                acceptable_keys=list(props_data.keys()),
                **kwargs,
            )
        # TODO Finish validating context panes
        if variant == "context":
            CustomKeyValidator(
                data=props_data,
                log=self.log,
                prepend_path=["props"],
                validator=PropValidator,
                is_context=True,
                **kwargs,
            )
            CustomKeyValidator(
                data=self.data.get("data", {}),
                log=self.log,
                prepend_path=["data"],
                validator=PanesContextDataValidator,
                prop_options=list(props_data.keys()),
                **kwargs,
            )
