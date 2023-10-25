"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
from cave_utils.api.general import props, values, layout
import type_enforced


@type_enforced.Enforcer
class panes_data_star(ApiValidator):
    """
    ## Api Path: panes.data.*
    """

    @staticmethod
    def spec(
        name: str, props: dict, values: [dict, None] = None, layout: [dict, None] = None, **kwargs
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the pane.
        - `props`:
            - Type: dict
            - What: The props that will be rendered in the pane.
            - See: `cave_utils.api.general.props`
        - `values`:
            - Type: dict
            - What: The values that will be passed to the props.
            - Required: False
            - See: `cave_utils.api.general.values`
        - `layout`:
            - Type: dict
            - What: The layout of the pane.
            - Required: False
            - See: `cave_utils.api.general.layout`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        # Validate Props
        CustomKeyValidator(
            data=self.data.get("props", {}),
            log=self.log,
            prepend_path=["props"],
            validator=props,
            **kwargs,
        )
        props_data = self.data.get("props", {})
        layout(
            data=self.data.get("layout", {}),
            log=self.log,
            prepend_path=["layout"],
            prop_id_list=list(props_data.keys()),
            **kwargs,
        )
        values(
            data=self.data.get("values", {}),
            log=self.log,
            prepend_path=["values"],
            props_data=props_data,
            **kwargs,
        )


@type_enforced.Enforcer
class panes(ApiValidator):
    """
    ## Api Path: panes
    """

    @staticmethod
    def spec(data: dict = dict(), **kwargs):
        """
        Optional Arguments:

        - `data`:
            - Type: dict
            - What: The data to pass to `panes.data.*`.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=panes_data_star, **kwargs
        )
