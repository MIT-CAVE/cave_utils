"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import *
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
            - See: `cave_utils.api.utils.PropValidator`
        - `values`:
            - Type: dict
            - What: The values that will be passed to the props.
            - Required: False
            - See: `cave_utils.api.utils.PropValueValidator`
        - `layout`:
            - Type: dict
            - What: The layout of the pane.
            - Required: False
            - See: `cave_utils.api.utils.PropLayoutValidator`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        # Validate Props
        CustomKeyValidator(
            data=self.data.get("props", {}),
            log=self.log,
            prepend_path=["props"],
            validator=PropValidator,
            **kwargs,
        )
        props_data = self.data.get("props", {})
        PropLayoutValidator(
            data=self.data.get("layout", {}),
            log=self.log,
            prepend_path=["layout"],
            prop_id_list=list(props_data.keys()),
            **kwargs,
        )
        PropValueValidator(
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
