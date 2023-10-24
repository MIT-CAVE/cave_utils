"""
General API Spec items that are found in multiple places. This is not a key that should be passed as part of your `session_data`.
"""
from pamda import pamda
import type_enforced
from cave_utils.api.utils import ApiValidator, CustomKeyValidator

@type_enforced.Enforcer
class props(ApiValidator):
    @staticmethod
    def spec(
        name: str,
        type: str,
        help: [str, None] = None,
        variant: [str, None] = None,
        enabled: [bool, None] = None,
        apiCommand: [str, None] = None,
        apiCommandKeys: [list, None] = None,
        options: [dict, None] = None,
        placeholder: [str, None] = None,
        maxValue: [float, int, None] = None,
        minValue: [float, int, None] = None,
        numberFormat: [dict, None] = None,
        maxRows: [int, None] = None,
        minRows: [int, None] = None,
        rows: [int, None] = None,
        notation: [str, None] = None,
        precision: [int, None] = None,
        notationDisplay: [str, None] = None,
        unit: [str, None] = None,
        views: [list, None] = None,
        legendNotation: [str, None] = None,
        legendPrecision: [int, None] = None,
        legendNotationDisplay: [str, None] = None,
        legendMinLabel: [str, None] = None,
        legendMaxLabel: [str, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the prop.
        - `type`:
            - Type: str
            - What: The type of the prop.
            - Accepted Values:
                - `"head"`
                - `"num"`
                - `"toggle"`
                - `"button"`
                - `"text"`
                - `"selector"`
                - `"date"`
                - `"media"`

        Optional Arguments:

        - `help`:
            - Type: str | None
            - What: The help text to display.
            - Default: `None`
        - `variant`:
            - Type: str | None
            - What: The variant of the prop.
            - Accepted Values:
                - Type: `"head"`
                    - `"column"`
                    - `"row"`
                - Type: `"text"`
                    - `"textarea"`
                - Type: `"num"`
                    - `"slider"`
                - Type: `"selector"`
                    - `"dropdown"`
                    - `"checkbox"`
                    - `"radio"`
                    - `"combobox"`
                    - `"hstepper"`
                    - `"vstepper"`
                    - `"hradio"`
                    - `"nested"`
                - Type: `"date"`
                    - `"date"`
                    - `"time"`
                    - `"datetime"`
                - Type: `"media"`
                    - `"picture"`
                    - `"video"`
            - Default: `None`
            - TODO: Check this
        - `enabled`:
            - Type: bool | None
            - What: If `True`, the prop will be enabled.
            - Default: `None`
            - Note: If `None`, the prop will be enabled.
        - `apiCommand`:
            - Type: str | None
            - What: The name of the api command to trigger.
            - Default: `None`
            - Note: if `None`, no `apiCommand` is triggered
        - `apiCommandKeys`:
            - Type: list | None
            - What: The top level api keys to pass to your `execute_command` if an apiCommand is provded.
            - Default: `None`
            - Note: If `None` all api keys are passed to your `execute_command`.
        - `options`:
            - Type: dict | None
            - What: The options for the prop. This only applies to `selector` props.
            - Default: `None`
            - Note: If `None`, no options are provided.
            - Note: Only options provided here are valid for the prop value.
        - `placeholder`:
            - Type: str | None
            - What: The placeholder text to display. This only applies to `text` props.
            - Default: `None`
            - Note: If `None`, no placeholder text is provided.
        - `maxValue`:
            - Type: float | int | None
            - What: The maximum value for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no maximum value is provided.
        - `minValue`:
            - Type: float | int | None
            - What: The minimum value for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no minimum value is provided.
        - `numberFormat`:
            - Type: dict | None
            - What: The number format for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no number format is provided.
            - TODO: Check / Extend this.
        - `maxRows`:
            - Type: int | None
            - What: The maximum number of rows to show for a `textarea` variant. This only applies to `text` props.
            - Default: `None`
            - Note: If `None`, no maximum number of rows is provided.
        - `minRows`:
            - Type: int | None
            - What: The minimum number of rows to show for a `textarea` variant. This only applies to `text` props.
            - Default: `None`
            - Note: If `None`, no minimum number of rows is provided.
        - `rows`:
            - Type: int | None
            - What: The number of rows to show for a `textarea` variant. This only applies to `text` props.
            - Default: `None`
            - Note: If `None`, no number of rows is provided.
        - `notation`:
            - Type: str | None
            - What: The notation to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no notation is provided.
            - TODO: Check / Extend This.
        - `precision`:
            - Type: int | None
            - What: The precision to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no precision is provided.
            - TODO: Check / Extend This.
        - `notationDisplay`:
            - Type: str | None
            - What: The notation display to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no notation display is provided.
            - TODO: Check / Extend This.
        - `unit`:
            - Type: str | None
            - What: The unit to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no unit is provided.
            - TODO: Check / Extend This.
        - `views`:
            - Type: list | None
            - What: A list of the views to use for the prop. This only applies to `date` props.
            - Default: `None`
            - Note: If `None`, no views are provided.
            - Valid Values: `["day", "hours", "minutes"]`
            - TODO: Check / Extend This.
        - `legendNotation`:
            - Type: str | None
            - What: The legend notation to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no legend notation is provided.
            - TODO: Check / Extend This.
        - `legendPrecision`:
            - Type: int | None
            - What: The legend precision to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no legend precision is provided.
            - TODO: Check / Extend This.
        - `legendNotationDisplay`:
            - Type: str | None
            - What: The legend notation display to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no legend notation display is provided.
            - TODO: Check / Extend This.
        - `legendMinLabel`:
            - Type: str | None
            - What: The legend minimum label to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no legend minimum label is provided.
            - TODO: Check / Extend This.
        - `legendMaxLabel`:
            - Type: str | None
            - What: The legend maximum label to use for the prop. This only applies to `num` props.
            - Default: `None`
            - Note: If `None`, no legend maximum label is provided.
            - TODO: Check / Extend This.
        """
        passed_values = {k: v for k, v in locals().items() if (v is not None) and k != "kwargs"}
        required_fields = ["name", "type"]
        optional_fields = ["help", "variant", "enabled"]
        if type != "head":
            optional_fields += ["apiCommand", "apiCommandKeys"]
        if type == "text":
            optional_fields += ["minRows", "maxRows", "rows"]
        if type == "num":
            if variant == "slider":
                required_fields += ["maxValue", "minValue"]
            else:
                optional_fields += ["maxValue", "minValue"]
            optional_fields += [
                "unit",
                "numberFormat",
                "notation",
                "precision",
                "notationDisplay",
                "legendNotation",
                "legendPrecision",
                "legendNotationDisplay",
                "legendMinLabel",
                "legendMaxLabel",
            ]
        if type == "selector":
            required_fields += ["options"]
            optional_fields += ["placeholder"]
        if type == "date":
            optional_fields += ["views"]
        missing_required = pamda.difference(required_fields, list(passed_values.keys()))
        if len(missing_required) > 0:
            raise Exception(f"Missing required fields: {str(missing_required)}")
        for k, v in passed_values.items():
            if k not in required_fields + optional_fields:
                kwargs[k] = v
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "type": ["head", "num", "toggle", "button", "text", "selector", "date", "media"],
                "views": ["year", "month", "day", "hours", "minutes", "seconds"],
                "legendNotation": ["compact", "precision", "scientific"],
                # TODO: Valiate These
                # TODO: Add Other value checks here
                "variant": {
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
                }.get(type, []),
            },
        }

    def __extend_spec__(self, **kwargs):
        if self.data.get("type") == "selector":
            CustomKeyValidator(
                data=self.data.get("options", {}),
                log=self.log,
                prepend_path=["options"],
                validator=props_options,
                variant=self.data.get("variant"),
                **kwargs,
            )


class props_options(ApiValidator):
    @staticmethod
    def spec(name: str, path: [list, None] = None, **kwargs):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the option.
        - `path`:
            - Type: list | None
            - What: The path to the option. This is only required for nested options.
            - Default: `None`
            - Note: If `None`, the option will not be selectable.
        """
        variant = kwargs.get("variant")
        kwargs = {k:v for k,v in kwargs.items() if k != "variant"}
        if variant == "nested":
            if path is None:
                raise Exception("Must provide a path for nested options")
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        if kwargs.get("variant") == "nested":
            if not isinstance(self.data.get("path"), list):
                self.__error__(
                    msg="`path` must be specified and a list of strings for nested options"
                )
                return
            self.__check_list_valid__(
                data=self.data.get("path", []), types=(str,), prepend_path=["path"]
            )


@type_enforced.Enforcer
class layout(ApiValidator):
    @staticmethod
    def spec(
        type: str,
        numColumns: [str, int, None] = None,
        numRows: [str, int, None] = None,
        data: [dict, None] = None,
        itemId: [str, None] = None,
        column: [int, None] = None,
        row: [int, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `type`:
            - Type: str
            - What: The type of the layout.
            - Accepted Values:
                - `"grid"`
                - `"item"`

        Optional Arguments:

        - `numColumns`:
            - Type: str | int
            - What: The number of columns for the grid layout. This only applies to `grid` layouts.
            - Default: `"auto"`
            - Note: If `"auto"`, the number of columns will be calculated based on the number of items.
        - `numRows`:
            - Type: str | int
            - What: The number of rows for the grid layout. This only applies to `grid` layouts.
            - Default: `"auto"`
            - Note: If `"auto"`, the number of rows will be calculated based on the number of items.
        - `data`:
            - Type: dict | None
            - What: The data for the layout. This only applies to `grid` layouts.
            - Default: `None`
            - Note: If `None`, no data is provided.
            - Accepted Values:
                - The prop keys from your api spec at the same level as `layout`.
        - `itemId`:
            - Type: str | None
            - What: The id of the item for the layout. This only applies to `item` layouts.
            - Default: `None`
            - Note: If `None`, no item id is provided.
        - `column`:
            - Type: int | None
            - What: The column in which to place this object in the current grid.
            - Default: `None`
            - Note: If `None`, no column is provided.
        - `row`:
            - Type: int | None
            - What: The row in which to place this object in the current grid.
            - Default: `None`
            - Note: If `None`, no row is provided.
        """
        passed_values = {k: v for k, v in locals().items() if (v is not None) and k != "kwargs"}
        if type == "grid":
            required_fields = ["type", "data"]
            optional_fields = ["numColumns", "numRows", "column", "row"]
        if type == "item":
            required_fields = ["type", "itemId"]
            optional_fields = ["column", "row"]
        missing_required = pamda.difference(required_fields, list(passed_values.keys()))
        if len(missing_required) > 0:
            raise Exception(f"Missing required fields: {str(missing_required)}")
        for k, v in passed_values.items():
            if k not in required_fields + optional_fields:
                kwargs[k] = v
        accepted_values = {
            "type": ["grid", "item"],
        }
        if isinstance(numRows, str):
            accepted_values["numRows"] = ["auto"]
        if isinstance(numColumns, str):
            accepted_values["numColumns"] = ["auto"]
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "type": ["grid", "item"],
            },
        }

    def __extend_spec__(self, **kwargs):
        layout_type = self.data.get("type", None)
        if layout_type == "grid":
            for field, value in self.data.get("data", {}).items():
                layout(
                    data=value, log=self.log, prepend_path=["data", field], **kwargs
                )
        if layout_type == "item":
            item_id = self.data.get("itemId", None)
            prop_id_list = kwargs.get("prop_id_list", [])
            if item_id not in prop_id_list:
                self.__error__(
                    msg=f"`itemId` ({item_id}) does not match any valid prop ids {prop_id_list}"
                )


@type_enforced.Enforcer
class values(ApiValidator):
    @staticmethod
    def spec(**kwargs):
        """
        Accepts all arbitrary values depending on what you have in your props as part of the api spec.

        The values you pass will be validated against the props in your api spec.
        """
        return {
            "kwargs": {},
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        props_data = kwargs.get("props_data", {})
        for prop_key, prop_value in self.data.items():
            prop_spec = props_data.get(prop_key, {})
            if not prop_spec:
                self.__error__(
                    msg=f"`{prop_key}` does not match any valid prop ids {list(props_data.keys())}"
                )
                continue
            prop_type = prop_spec.get("type", None)
            acceptable_types = {
                "head": (str,),
                "num": (int, float),
                "toggle": (bool,),
                "button": (str,),
                "text": (str,),
                "selector": (list,),
                "date": (str,),
                "media": (str,),
            }.get(prop_type, None)
            if not self.__check_type__(prop_value, acceptable_types, prepend_path=[prop_key]):
                continue
            if prop_type == "num":
                min_value = prop_spec.get("minValue", float("-inf"))
                max_value = prop_spec.get("maxValue", float("inf"))
                if prop_value < min_value or prop_value > max_value:
                    self.__error__(
                        msg=f"`{prop_key}` with the prop type of `{prop_type}` must be between {min_value} and {max_value} as defined by the api spec."
                    )
            elif prop_type == "selector":
                options = list(prop_spec.get("options", {}).keys())
                self.__check_subset_valid__(prop_value, options, prepend_path=[prop_key])
            elif prop_type == "head":
                self.__error__(
                    msg=f"`{prop_key}` with the prop type of `{prop_type}` can not have an associated value."
                )
            elif prop_type == "date":
                pass
                # TODO: Validate date string
            elif prop_type == "media":
                self.__check_url_valid__(prop_value)


class GeoJsonValidator(ApiValidator):
    def __populate_data__(self, **kwargs):
        self.field_types = {
            "geoJsonLayer": str,
            "geoJsonProp": str,
        }
        self.required_fields = ["geoJsonLayer", "geoJsonProp"]
        self.optional_fields = []
        self.accepted_values = {}

    def __extend_spec__(self, **kwargs):
        self.__check_url_valid__(
            url=self.data.get("geoJsonLayer", None), prepend_path=["geoJsonLayer"]
        )

