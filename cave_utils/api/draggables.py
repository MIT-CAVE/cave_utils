"""
Configure the state of draggable UI elements (floating panels, time control, etc.).
"""

from cave_utils.api_utils.validator_utils import ApiValidator, CustomKeyValidator
import type_enforced


@type_enforced.Enforcer
class draggables(ApiValidator):
    """
    The draggables are located under the path **`draggables`**.
    """

    @staticmethod
    def spec(data: dict, **kwargs):
        """
        Arguments:

        * **`data`**: `[dict]` &rarr; A dictionary of draggable items to configure.
            * **See**: `cave_utils.api.draggables.draggables_data_star`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        CustomKeyValidator(
            data=self.data.get("data", {}),
            log=self.log,
            prepend_path=["data"],
            validator=draggables_data_star,
            **kwargs,
        )


@type_enforced.Enforcer
class draggables_data_star(ApiValidator):
    """
    The draggable item configuration is located under the path **`draggables.data.*`**.
    """

    @staticmethod
    def spec(
        open: bool | None = None,
        position: dict | None = None,
        hideCloseOption: bool | None = None,
        hideDragOption: bool | None = None,
        showDragHandle: bool | None = None,
        hideCloseButton: bool | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`open`**: `[bool]` = `None` &rarr; If `True`, the draggable will be visible when the application loads.
            * **Note**: If left unspecified (i.e., `None`), the default visibility is determined by the application.
        * **`position`**: `[dict]` = `None` &rarr; The initial pixel position of the draggable on screen.
            * **See**: `cave_utils.api.draggables.draggables_data_star_position`
            * **Note**: If left unspecified (i.e., `None`), the default position is determined by the application.
        * **`hideCloseOption`**: `[bool]` = `None` &rarr; If `True`, the close button will be hidden on the draggable.
            * **Note**: If left unspecified (i.e., `None`), the close button is shown by default.
        * **`hideDragOption`**: `[bool]` = `None` &rarr; If `True`, the drag handle will be hidden on the draggable.
            * **Note**: If left unspecified (i.e., `None`), the drag handle is shown by default.
        * **`showDragHandle`**: `[bool]` = `None` &rarr; If `True`, the drag handle will be shown on the draggable.
            * **Note**: If left unspecified (i.e., `None`), the drag handle visibility is determined by the application.
        * **`hideCloseButton`**: `[bool]` = `None` &rarr; If `True`, the close button will be hidden on the draggable.
            * **Note**: If left unspecified (i.e., `None`), the close button visibility is determined by the application.
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        position = self.data.get("position")
        if position is not None:
            draggables_data_star_position(
                data=position,
                log=self.log,
                prepend_path=["position"],
                **kwargs,
            )


@type_enforced.Enforcer
class draggables_data_star_position(ApiValidator):
    """
    The draggable position is located under the path **`draggables.data.*.position`**.
    """

    @staticmethod
    def spec(x: int, y: int, **kwargs):
        """
        Arguments:

        * **`x`**: `[int]` &rarr; The horizontal offset in pixels from the left edge of the application (excluding the app bar).
        * **`y`**: `[int]` &rarr; The vertical offset in pixels from the top edge of the screen.
        """
        return {"kwargs": kwargs, "accepted_values": {}}
