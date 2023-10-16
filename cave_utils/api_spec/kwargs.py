from cave_utils.api_spec.utils import *

class kwargs(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "wipeExisting": bool,
        }

        self.accepted_values = {}

        self.required_fields = []

        self.optional_fields = ["wipeExisting"]