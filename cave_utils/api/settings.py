"""
Configure general settings for your application like the icons to use, how to sync data with the server, and more.
"""
from cave_utils.api_utils.validator_utils import *
import type_enforced


@type_enforced.Enforcer
class settings(ApiValidator):
    """
    The settings are located under the path **`settings`**.
    """

    @staticmethod
    def spec(
        iconUrl: str,
        demo: dict = dict(),
        sync: dict = dict(),
        time: dict = dict(),
        defaults: dict = dict(),
        debug: bool = False,
        **kwargs,
    ):
        """
        Arguments:

        * **`iconUrl`**: `[str]` &rarr; The URL to the icon bundle for your application.
            * **Example**: `"https://react-icons.mitcave.com/4.10.1"`.
            * **Note**: This is the only required attribute in `settings`.
        * **`demo`**: `[dict]` = `{}` &rarr; Settings for the demo mode of your application.
            * **See**: `settings_demo`.
        * **`sync`**: `[dict]` = `{}` &rarr; Settings for syncing data with the server.
            * **See**: `settings_sync`.
        * **`time`**: `[dict]` = `{}` &rarr; Settings for the time display.
            * **See**: `settings_time`.
        * **`defaults`**: `[dict]` = `{}` &rarr; Default settings for your application.
            * **See**: `settings_defaults`.
        * **`debug`**: `[dict]` = `{}` &rarr; If `True`, the CAVE App client will show additional information for debugging purposes.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        self.__check_url_valid__(
            url=self.data.get("iconUrl"),
        )
        CustomKeyValidator(
            data=self.data.get("sync", {}),
            log=self.log,
            prepend_path=["sync"],
            validator=settings_sync,
            **kwargs,
        )
        CustomKeyValidator(
            data=self.data.get("demo", {}),
            log=self.log,
            prepend_path=["demo"],
            validator=settings_demo,
            **kwargs,
        )
        if self.data.get("time"):
            settings_time(
                data=self.data.get("time", {}),
                log=self.log,
                prepend_path=["time"],
                **kwargs,
            )
        settings_defaults(
            data=self.data.get("defaults", {}),
            log=self.log,
            prepend_path=["defaults"],
            **kwargs,
        )


@type_enforced.Enforcer
class settings_demo(ApiValidator):
    """
    The demo settings are located under the path **`settings.demo`**.
    """

    @staticmethod
    def spec(scrollSpeed: [int, float] = 1, displayTime: int = 5, **kwargs):
        """
        Arguments:

        TODO: Review this definition. Before, we had:
        A float value representing degrees of rotation per frame (degrees per 13 milliseconds). This key only applies to map views

        * **`scrollSpeed`**: `[int, float]` = `1` &rarr; The speed at which the demo text will scroll.
        * **`displayTime`**: `[int]` = `5` &rarr; The time duration in seconds to display the demo text.
        """
        return {"kwargs": kwargs, "accepted_values": {}}


@type_enforced.Enforcer
class settings_sync(ApiValidator):
    """
    The sync settings are located under the path **`settings.sync`**.
    """

    @staticmethod
    def spec(name: str, showToggle: bool, value: bool, data: dict, **kwargs):
        """
        Arguments:

        * **`name`**: `[str]` &rarr; The name of the sync setting.
        * **`showToggle`**: `[bool]` &rarr; If `True`, the toggle will be displayed.
        * **`value`**: `[bool]` &rarr; The initial value of the toggle.
        * **`value`**: `[dict]` &rarr; The data to sync with the server.
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    # def __extend_spec__(self, **kwargs):
    #     root_data = kwargs.get("root_data", {})
    #     for key, path in self.data.get("data", {}).items():
    #         if not pamda.hasPath(path, root_data):
    #             self.__warn__(f"Path {path} does not exist.", prepend_path=["data", key])


@type_enforced.Enforcer
class settings_time(ApiValidator):
    """
    The time settings are located under the path **`settings.time`**.
    """

    @staticmethod
    def spec(timeLength: int, timeUnits: str, **kwargs):
        """
        Arguments:

        * **`timeLength`**: `[int]` &rarr; The amount of time values to display.
        * **`timeUnits`**: `[str]` &rarr; The units of time to display.
            * **Example**: `"Decade"`.
        """
        return {"kwargs": kwargs, "accepted_values": {}}


@type_enforced.Enforcer
class settings_defaults(ApiValidator):
    """
    The defaults settings are located under the path **`settings.defaults`**.
    """

    @staticmethod
    def spec(
        precision: int = 2,
        trailingZeros: bool = False,
        unitPlacement: str = "right",
        showToolbar: bool = True,
        **kwargs,
    ):
        """
        Arguments:

        * **`precision`**: `[int]` = `2` &rarr; The number of decimal places to display.
        * **`trailingZeros`**: `[bool]` = `False` &rarr; If `True`, trailing zeros will be displayed.
        * **`unitPlacement`**: `[str]` = `"afterWithSpace"` &rarr; The position of the `unit` symbol relative to the value.
            * **Accepted values**:
                    * `"after"`: The `unit` appears after the value.
                    * `"afterWithSpace"`: The `unit` appears after the value, separated by a space.
                    * `"before"`: The `unit` appears before the value.
                    * `"beforeWithSpace"`: The unit is placed before the value, with a space in between.
        * **`showToolbar`**: `[bool]` = `True` &rarr; If `True`, chart toolbars will be displayed by default.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "unitPlacement": ["after", "afterWithSpace", "before", "beforeWithSpace"],
            },
        }
