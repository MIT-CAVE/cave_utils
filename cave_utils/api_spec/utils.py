from pamda import pamda
import re
from cave_utils.log import LogHelper, LogObject

class ApiValidator:
    def __init__(self, data, log: LogObject, prepend_path: list = list(), **kwargs):
        self.data = data
        self.ignore_keys = kwargs.get("ignore_keys", set())
        self.log = LogHelper(log=log, prepend_path=prepend_path)
        self.__populate_data__(**kwargs)
        self.validate(**kwargs)

    def validate(self, **kwargs):
        for field in self.required_fields:
            if field not in self.data:
                self.log.add(path=[field], msg=f"Missing required field: ({field})")
        for field, value in self.data.items():
            if field in self.ignore_keys:
                continue
            if field in ['timeValues', 'order']:
                continue
                # TODO: Implement validation for these fields
            accepted_values = self.accepted_values.get(field, None)
            if (
                isinstance(
                    value,
                    (
                        list,
                        dict,
                    ),
                )
                and accepted_values is not None
            ):
                check_value = value
                if isinstance(value, dict):
                    check_value = list(value.keys())
                value_diff = pamda.difference(check_value, accepted_values)
                if len(value_diff) > 0:
                    self.log.add(
                        path=[field],
                        msg=f"Invalid values ('{value_diff}'): Acceptable values are: {accepted_values}",
                    )
                    continue
            else:
                if accepted_values is not None and value not in accepted_values:
                    self.log.add(
                        path=[field],
                        msg=f"Invalid value ('{value}'): Acceptable values are: {accepted_values}",
                    )
                    continue
            if field not in self.required_fields + self.optional_fields:
                self.log.add(
                    path=[field],
                    msg=f"Unknown field ('{field}'): Acceptable fields are: {self.required_fields + self.optional_fields}",
                    level="warning",
                )
                continue
            acceptable_types = self.field_types.get(field, type(None))
            if not isinstance(value, acceptable_types):
                self.log.add(
                    path=[field],
                    msg=f"Invalid type ('{type(value)}'): Acceptable types are: {acceptable_types}",
                )

        # Run additional Validations
        # self.__additional_validations__(**kwargs)
        try:
            self.__additional_validations__(**kwargs)
        except Exception as e:
            self.log.add(
                path=[],
                msg=f"Additional validations failed (likely due to another error with your api data)",
            )

    def __additional_validations__(self, **kwargs):
        pass

    def error(self, error: str, prepend_path: list = []):
        self.log.add(path=prepend_path, msg=error)

    def warn(self, error: str, prepend_path: list = []):
        self.log.add(path=prepend_path, msg=error, level="warning")

    # Add Special Validator Checks
    def check_rgba_string_valid(self, rgba_string: str, prepend_path:list=[]):
        try:
            if "rgba(" != rgba_string[:5]:
                self.log.add(path=prepend_path, msg="Invalid RGBA string")
                return
            if ")" != rgba_string[-1]:
                self.log.add(path=prepend_path, msg="Invalid RGBA string")
                return
            rgba_list = rgba_string[5:-1].replace(" ", "").split(",")
            for rgba in rgba_list:
                if not rgba.isdigit():
                    self.log.add(path=prepend_path, msg="Invalid RGBA string")
                    return
                if int(rgba) < 0 or int(rgba) > 255:
                    self.log.add(path=prepend_path, msg="Invalid RGBA string")
                    return
        except:
            self.log.add(path=prepend_path, msg="Invalid RGBA string")

    def check_pixel_string_valid(self, pixel_string: str, prepend_path:list=[]):
        try:
            if "px" != pixel_string[-2:]:
                self.log.add(path=prepend_path, msg="Invalid pixel string")
                return
            if int(pixel_string[:-2]) <= 0:
                self.log.add(path=prepend_path, msg="Invalid pixel string")
        except:
            self.log.add(path=prepend_path, msg="Invalid pixel string")

    def check_url_valid(self, url: str, prepend_path:list=[]):
        # Use Django regex for URL validation
        # See https://stackoverflow.com/a/7160778/12014156
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if re.match(regex, url) is None:
            self.log.add(path=prepend_path, msg="Invalid url")

    def check_subset_valid(self, subset: list, valid_values: list, prepend_path:list=[]):
        invalid_values = pamda.difference(subset, valid_values)
        if len(invalid_values) > 0:
            self.log.add(path=prepend_path, msg="Invalid values selected: " + str(invalid_values))

    def check_coord_path_valid(self, coord_path: list, prepend_path:list=[]):
        try:
            if len(coord_path) < 2:
                self.log.add(path=prepend_path, msg="Invalid coordinate path")
                return
            for coord in coord_path:
                # Ensure coord is less than 3 items (longitude, latitude, altitude)
                if len(coord) > 3:
                    self.log.add(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Longitude
                if coord[0] < -180 or coord[0] > 180:
                    self.log.add(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Latitude
                if coord[1] < -90 or coord[1] > 90:
                    self.log.add(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Altitude (if present)
                if len(coord) == 3:
                    if coord[2] < 0:
                        self.log.add(path=prepend_path, msg="Invalid coordinate path")
                        return
        except:
            self.log.add(path=prepend_path, msg="Invalid coordinate path")

    def check_list_valid(self, data: list, types: tuple, prepend_path:list=[]):
        if not isinstance(types, tuple):
            types = (types,)
        for idx, item in enumerate(data):
            if not isinstance(item, types):
                self.log.add(path=prepend_path, msg=f"Invalid list item type at index: {idx} with type: {type(item)}")
                return


class ColorByOptionValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "min": (float, int),
            "max": (float, int),
            "startGradientColor": str,
            "endGradientColor": str,
            "nullColor": (str, type(None)),
        }
        self.required_fields = ["startGradientColor", "endGradientColor"]
        self.optional_fields = ["min", "max", "nullColor"]
        self.accepted_values = {}

    def __additional_validations__(self, **kwargs):
        for field in ["startGradientColor", "endGradientColor"]:
            self.check_rgba_string_valid(
                rgba_string=self.data.get(field),
                prepend_path=[field]
            )


class SizeByOptionValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "min": (float, int),
            "max": (float, int),
            "nullSize": (str, type(None)),
            "startSize": str,
            "endSize": str,
        }
        self.required_fields = ["startSize", "endSize"]
        self.optional_fields = ["min", "max", "nullSize"]
        self.accepted_values = {}

    def __additional_validations__(self, **kwargs):
        for field in ["startSize", "endSize", "nullSize"]:
            field_value = self.data.get(field)
            if field_value is not None:
                self.check_pixel_string_valid(
                    pixel_string=field_value, 
                    prepend_path=[field]
                )
        

class CustomKeyValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {i: dict for i in self.data.keys()}
        self.required_fields = list(self.data.keys())
        self.optional_fields = []
        self.accepted_values = {}

    def __additional_validations__(self, **kwargs):
        assert "validator" in kwargs, "Must pass validator to CustomKeyValidator"
        validator = kwargs.get("validator")
        kwargs_new = {k:v for k,v in kwargs.items() if k != "validator"}
        for field, value in self.data.items():
            validator(data=value, log=self.log, prepend_path=[field], **kwargs_new)


class PropValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        validation_type = self.data.get("type")
        variant = self.data.get("variant")

        self.field_types = {
            "name": str,
            "help": str,
            "type": str,
            "variant": str,
            # General
            "enabled": bool,
            "apiCommand": str,
            "apiCommandKeys": list,
            # Type Specific
            "options": dict,
            "placeholder": str,
            "maxValue": (int, float),
            "minValue": (int, float),
            "numberFormat": dict,
            "maxRows": int,
            "minRows": int,
            "rows": int,
            "notation": str,
            "precision": int,
            "notationDisplay": str,
            "unit": str,
            # Legend Specific
            "legendNotation": str,
            "legendPrecision": int,
            "legendNotationDisplay": str,
            "legendMinLabel": str,
            "legendMaxLabel": str,
        }

        self.allowed_variants = {
            "head": ["column", "row"],
            "text": ["textarea"],
            "num": ["slider"],
            "selector": [
                "dropdown",
                "checkbox",
                "radio",
                "combobox",
                "hstepper",
                "vstepper",
                "hradio",
                "nested",
            ],
            "date": ["date", "time", "datetime"],
            "media": ["picture", "video"],
        }

        self.accepted_values = {
            "type": ["head", "num", "toggle", "button", "text", "selector", "date", "media"],
            "variant": self.allowed_variants.get(validation_type, []),
            "views": ["year", "day", "hours", "minutes"],
            "legendNotation": ['compact', 'precision', 'scientific'],
        }

        self.required_fields = ["name", "type"]

        self.optional_fields = ['help', 'variant', 'enabled']

        if validation_type != "head":
            self.optional_fields += ["apiCommand", "apiCommandKeys"]
        if validation_type == "text":
            self.optional_fields += ["minRows", "maxRows", "rows"]
        if validation_type == "num":
            if variant == "slider":
                self.required_fields += ["maxValue", "minValue"]
            else:
                self.optional_fields += ["maxValue", "minValue"]
            self.optional_fields += ["unit", "numberFormat", "notation", "precision", "notationDisplay", "legendNotation", "legendPrecision", "legendNotationDisplay", "legendMinLabel", "legendMaxLabel"]
        if validation_type == "selector":
            self.required_fields += ["options"]
            self.optional_fields += ["placeholder"]
            self.accepted_values["value"] = list(self.data.get("options", {}).keys())
        if validation_type == "date":
            self.optional_fields += ["views"]

    def __additional_validations__(self, **kwargs):
        if self.data.get("type") == "selector":
            CustomKeyValidator(
                data=self.data.get("options", {}),
                log=self.log,
                prepend_path=["options"],
                validator=SelectorOptionsValidator,
                variant = self.data.get("variant"),
                **kwargs,
            )


class SelectorOptionsValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "name": str,
            "path": list,
        }
        self.required_fields = ["name"]
        self.optional_fields = []
        self.accepted_values = {}
        if kwargs.get("variant") == "nested":
            self.required_fields += ["path"]

    def __additional_validations__(self, **kwargs):
        self.check_list_valid(
            data=self.data.get("path", []), 
            types=(str,), 
            prepend_path=["path"]
        )


class LayoutValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        layout_type = self.data.get("type", None)

        self.field_types = {
            "type": str,
            "numColumns": (str, int),
            "numRows": (str, int),
            "data": dict,
            "itemId": str,
            "column": int,
            "row": int,
        }

        self.accepted_values = {
            "type": ["grid", "item"],
        }

        self.required_fields = ['type']
        self.optional_fields = []

        if layout_type == "grid":
            self.required_fields += ["numColumns", "numRows", "data"]
            self.optional_fields += []

        if layout_type == "item":
            self.required_fields += ["type", "itemId"]
            self.optional_fields += ["column", "row"]
            self.accepted_values["itemId"] = kwargs.get("acceptable_keys", [])


        num_columns = self.data.get("numColumns", None)
        if isinstance(num_columns, str):
            if not num_columns.isdigit():
                self.accepted_values["numColumns"] = ["auto"]
        num_rows = self.data.get("numRows", None)
        if isinstance(num_rows, str):
            if not num_rows.isdigit():
                self.accepted_values["numRows"] = ["auto"]

    def __additional_validations__(self, **kwargs):
        layout_type = self.data.get("type", None)
        if layout_type == "grid":
            for field, value in self.data.get("data", {}).items():
                LayoutValidator(data=value, log=self.log, prepend_path=["data", field], **kwargs)


class GeoJsonValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "geoJsonLayer": str,
            "geoJsonProp": str,
        }
        self.required_fields = ["geoJsonLayer", "geoJsonProp"]
        self.optional_fields = []
        self.accepted_values = {}

    def __additional_validations__(self, **kwargs):
        self.check_url_valid(
            url = self.data.get("geoJsonLayer", None),
            prepend_path=["geoJsonLayer"]
        )


class ViewportValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        is_optional_viewport = kwargs.get("is_optional_viewport", False)
        self.field_types = {
            "latitude": (
                float,
                int,
            ),
            "longitude": (
                float,
                int,
            ),
            "zoom": (
                float,
                int,
            ),
            "bearing": (
                float,
                int,
            ),
            "pitch": (
                float,
                int,
            ),
            "height": (
                float,
                int,
            ),
            "altitude": (
                float,
                int,
            ),
            "maxZoom": (
                float,
                int,
            ),
            "minZoom": (
                float,
                int,
            ),
            "icon": str,
            "name": str,
            "order": int,
        }

        self.accepted_values = {}

        self.required_fields = ["latitude", "longitude", "zoom"]

        self.optional_fields = [
            "maxZoom",
            "minZoom",
            "height",
            "altitude",
            "bearing",
            "pitch",
            "order",
        ]

        if is_optional_viewport:
            self.required_fields += ["icon", "name"]
