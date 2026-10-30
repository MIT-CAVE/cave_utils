"""
General API Spec items that are found in multiple places. This is not a key that should be passed as part of your `session_data`.
"""

from pamda import pamda
import type_enforced
from cave_utils.api_utils.validator_utils import (
    ApiValidator,
    CustomKeyValidator,
    DATE_BOUND_FORMATS,
    DATE_BOUND_FORMAT_NAMES,
    DATETIME_BOUND_FORMATS,
    DATETIME_BOUND_FORMAT_NAMES,
    DATE_DEFAULT_VIEWS,
    DATE_DISABLED_DATE_FORMATS,
    DATE_DISABLED_DATE_FORMAT_NAMES,
    DATE_MONTH_NAMES,
    DATE_TIME_OF_DAY_FORMAT_NAMES,
    DATE_TIME_STEP_LIMITS,
    DATE_VIEW_NAMES,
    DATE_WEEKDAY_NAMES,
    SECONDS_PER_DAY,
)


@type_enforced.Enforcer
class props(ApiValidator):
    @staticmethod
    def spec(
        name: str,
        type: str,
        subtitle: str | None = None,
        help: str | None = None,
        helperText: str | None = None,
        variant: str | None = None,
        display: bool | None = None,
        enabled: bool | None = None,
        container: str | None = None,
        apiCommand: str | None = None,
        apiCommandKeys: list[str] | None = None,
        options: dict | None = None,
        valueOptions: list[int | float] | None = None,
        label: str | None = None,
        labelPlacement: str | None = None,
        activeLabel: str | None = None,
        placeholder: str | None = None,
        direction: str | None = None,
        defaultZoom: int | float | None = None,
        minZoom: int | float | None = None,
        maxZoom: int | float | None = None,
        maxBounds: list[list[int | float]] | None = None,
        pathColor: str | None = None,
        pathWeight: int | float | None = None,
        numVisibleTags: int | None = None,
        availableTitle: str | None = None,
        selectedTitle: str | None = None,
        height: int | float | str | None = None,
        maxValue: float | int | None = None,
        minValue: float | int | None = None,
        gradient: dict | None = None,
        fallback: dict | None = None,
        maxRows: int | None = None,
        minRows: int | None = None,
        rows: int | None = None,
        notation: str | None = None,
        precision: int | None = None,
        notationDisplay: str | None = None,
        unit: str | None = None,
        unitPlacement: str | None = None,
        views: list[str] | None = None,
        defaultView: str | None = None,
        minDate: str | None = None,
        maxDate: str | None = None,
        minTime: str | None = None,
        maxTime: str | None = None,
        minDateTime: str | None = None,
        maxDateTime: str | None = None,
        timezone: str | None = None,
        hoursStep: int | None = None,
        minutesStep: int | None = None,
        secondsStep: int | None = None,
        disabledTimes: list[list[str]] | None = None,
        disabledDates: list[str] | None = None,
        disabledWeekdays: list[int | str] | None = None,
        disabledMonths: list[int | str] | None = None,
        disabledYears: list[int] | None = None,
        dateOrder: str | None = None,
        hour24: bool | None = None,
        disablePast: bool | None = None,
        disableFuture: bool | None = None,
        legendNotation: str | None = None,
        legendPrecision: int | None = None,
        legendNotationDisplay: str | None = None,
        legendMinLabel: str | None = None,
        legendMaxLabel: str | None = None,
        icon: str | None = None,
        activeIcon: str | None = None,
        startIcon: str | None = None,
        endIcon: str | None = None,
        color: str | None = None,
        activeColor: str | None = None,
        size: str | None = None,
        activeSize: str | None = None,
        placement: str | None = None,
        fullWidth: bool | None = None,
        url: str | None = None,
        suppressCommand: bool | None = None,
        scaleMode: str | None = None,
        propStyle: dict | None = None,
        readOnly: bool | None = None,
        marks: dict[str, dict[str, str]] | None = None,
        trailingZeros: bool | None = None,
        locale: str | None = None,
        fallbackValue: str | None = None,
        draggable: bool | None = None,
        quickView: bool | None = None,
        allowNone: bool | None = None,
        marqueeLabel: bool | None = None,
        spinner: str | bool | None = None,
        smallStep: float | int | None = None,
        step: float | int | None = None,
        largeStep: float | int | None = None,
        hideKeyboardToggle: bool | None = None,
        scale: str | None = None,
        scaleParams: dict | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`name`**: `[str]` &rarr; The name of the prop.
        * **`type`**: `[str]` &rarr; The type of the prop.
            * **Accepted Values**:
                * `"head"`: A header for an individual section, containing a `title` and a `help` message
                * `"num"`: A numeric input field
                * `"toggle"`: A switch button to enable or disable a single setting
                * `"button"`: A regular button
                * `"text"`: A text input field
                * `"selector"`: Select options from a set
                * `"date"`: Select a date and/or time
                * `"media"`: View various media formats
                    * Note: A variant is required when using the `media` type
                * `"coordinate"`: A coordinate input field
        * **`subtitle`**: `[str]` = `None` &rarr; An optional subtitle for the prop.
        * **`help`**: `[str]` = `None` &rarr; The help text to display.
            * **Notes**:
                - This is displayed when the user clicks on the help icon next to the prop.
                - This can be regular text or markdown.
                - It is rendered as markdown unless `richText` is `False`. In the next major version, it will only be rendered as markdown when `richText` is `True`.
                - See `richText` in the `cave_utils.api` docs for more information.
                - HTML in the markdown is sanitized: scripts, iframes, event handlers, inline styles and classes are removed, as well as links with a protocol other than `http`, `https`, `mailto`, `irc`, `ircs` or `xmpp` (e.g. `javascript:`, `data:` or `tel:`). Relative links and links to the same page (`#id`) are kept.
        * **`helperText`**: `[str]` = `None` &rarr; Additional help text to display below the prop without requiring a click on the help icon.
        * **`display`**: `[bool]` = `None` &rarr; Whether or not the prop will be displayed.
        * **`variant`**: `[str]` = `None` &rarr; The variant of the prop.
            * **Accepted Values**:
                * When **`type`** == `"head"`:
                    * `"column"`: A header for a column of related prop items
                    * `"row"`: A header for a row of related prop items
                    * `"icon"`: **Deprecated**, will be removed in `4.0.0`, in favor of `"column"`.
                    * `"iconRow"`: **Deprecated**, will be removed in `4.0.0`, in favor of `"row"`.
                * When **`type`** == `"text"`:
                    * `"single"`: A single-line text input field
                    * `"textarea"`: A multi-line text input field
                * When **`type`** == `"num"`:
                    * `"field"`: A numeric input field
                    * `"slider"`: A range of values along a bar, from which users may select a single value
                    * `"icon"`: A fixed numerical value presented alongside a corresponding icon.
                    * `"iconCompact"`: Similar to `"icon"`, but designed in a compact format for appropriate rendering within a draggable pad.
                    * `"iconCompactAlt"`: Similar to `"iconCompact"`, but designed for rendering within a horizontally scrollable carousel (e.g. a global output docked to the persistent status bar).
                    * `"incslider"`: A range of values along a bar, from which users may select a single value, with a predefined set of options.
                * When **`type`** == `"selector"`:
                    * `"checkbox"`: Select one or more items from a set of checkboxes
                    * `"hcheckbox"`: A set of `"checkbox"`s placed horizontally
                    * `"combobox"`: A dropdown with a search bar allowing users to filter and select a single option by typing
                    * `"comboboxMulti"`: A dropdown with a search bar, enabling users to filter and select multiple options. Selected items are displayed as tags within the input field.
                    * `"dropdown"`: Show multiple options that appear when the element is clicked
                    * `"dualList"`: Select one or more options by moving them between two side-by-side lists: "available" and "selected"
                    * `"nested"`: Select one or more options from a set of nested checkboxes
                    * `"radio"`: Select one option from a set of mutually exclusive options
                    * `"hradio"`: A set of `"radio"`s placed horizontally
                    * `"hstepper"`: Select a unique option along a horizontal slider
                    * `"vstepper"`: Select a unique option along a vertical slider
                * When **`type`** == `"date"`:
                    * `"date"`: Select a date via a calendar pop-up that appears when the element is clicked (default)
                        * **Note**: Passed as `YYYY-MM-DD`
                    * `"time"`: Select a time via a clock pop-up that appears when the element is clicked
                        * **Note**: Passed as `HH:MM:SS`
                    * `"datetime"`: Select date and time via a pop-up with calendar and clock tabs that appear when the element is clicked
                        * **Note**: Passed as `YYYY-MM-DDTHH:MM:SS`
                * When **`type`** == `"media"`:
                    * `"picture"`: Show a PNG or JPG image
                    * `"video"`: Display a YouTube, Vimeo, or Dailymotion video clip
                    * `"audio"`: Play an audio clip (e.g. MP3, WAV, or OGG) with the browser's native audio player
                * When **`type`** == `"coordinate"`:
                    * `"latLngInput"`: **Deprecated** alias of `"latLngMap"`, will be removed in `4.0.0`.
                    * `"latLngMap"`: A map popup to select a latitude and longitude by dragging its marker
                    * `"latLngPath"`: A map popup to build a path of latitude and longitude points by dragging its marker or entering coordinates manually
        * **`container`**: `[str]` = `"vertical"` | `"none"` &rarr;
            * Specifies the type of prop container by selecting from predefined styles.
            * **Accepted Values**:
                * `"vertical"`: A vertical layout where the prop `name` appears at the top inside the container.
                * `"horizontal"`: A horizontal layout where the prop `name` is on the left, followed by the actionable prop on the right.
                * `"titled"`: Similar to the vertical container but without a background color, removing the embossed appearance of the prop.
                * `"untitled"`: A slim container version without the prop `name` or `unit` label.
                * `"none"`: Removes the prop container entirely, disabling the display of the prop `name`, `help` button and `unit` label. Only the actionable prop is displayed.
            * **Notes**:
                * This attribute applies to all props except the `"icon"` and `"iconCompact"` variants of the `"num"` prop.
                * If left unspecified (i.e., `None`), the default is `"none"` for `"head"` props, and `"vertical"` for all others. As stated, the `"icon"` and `"iconCompact"` variants of the `"num"` prop are always set to `"none"`, regardless of this attribute.
                * When the container is set to `"none"`, the `style` prop used at the `"item"` level of the `layout` becomes ineffective.
        * **`enabled`**: `[bool]` = `True` &rarr; Whether or not the prop will be enabled.
            * **Note**: This attribute applies to all props except `"head"` props.
        * **`apiCommand`**: `[str]` = `None` &rarr; The name of the API command to trigger.
            * **Note**: If `None`, no `apiCommand` is triggered.
            * **Note**: This attribute applies to all props except `"head"` props.
        * **`apiCommandKeys`**: `[list[str]]` = `None` &rarr;
            * The root API keys to pass to your `execute_command` function if an `apiCommand` is provided.
            * **Note**: If `None`, all API keys are passed to your `execute_command`.
            * **Note**: This attribute applies to all props except `"head"` props.
        * **`options`**: `[dict]` = `None` &rarr;
            * The options to be displayed on the UI element mapped to their display properties.
            * **Notes**:
                * Only options provided here are valid for the prop value
                * This attribute applies to only `"selector"` props
        * **`numVisibleTags`**: `[int]` = `None` &rarr;
            * The maximum number of tags visible in a `"comboboxMulti"` variant of a `"selector"` prop when it is not focused.
            * **Notes**:
                * If `None`, `1` tag will be displayed and any remaining selections are summarized in a `+N more` chip
                * This attribute applies exclusively to `"selector"` props using the `"comboboxMulti"` variant
        * **`availableTitle`**: `[str]` = `None` &rarr; The title displayed above the list of options that are not selected.
            * **Notes**:
                * If `None`, `"Available"` will be used
                * This attribute applies exclusively to `"selector"` props using the `"dualList"` variant
        * **`selectedTitle`**: `[str]` = `None` &rarr; The title displayed above the list of selected options.
            * **Notes**:
                * If `None`, `"Selected"` will be used
                * This attribute applies exclusively to `"selector"` props using the `"dualList"` variant
        * **`height`**: `[int | float | str]` = `None` &rarr; The height of the lists.
            * **Notes**:
                * A number is interpreted as pixels; a string can be any valid CSS height (e.g. `"20rem"`)
                * If `None`, `240` will be used
                * This attribute applies exclusively to `"selector"` props using the `"dualList"` variant
        * **`valueOptions`**: `[list[int|float]]` = `None` &rarr;
            * **Notes**:
                * Only valueOptions provided here can be selected for the prop value
                * This attribute applies to `"num"` props with the `"incslider"` variant.
        * **`label`**: `[str]` = `None` &rarr; The label to display above the input field when the prop is focused.
            * **Note**: This attribute applies to `"num"`, `"text"` and `"date"` props.
        * **`labelPlacement`**: `[str]` = `None` &rarr; The placement of the label relative to the input field.
            * **Accepted Values**:
                * `"start"`: The label is placed at the start of the input field.
                * `"end"`: The label is placed at the end of the input field.
                * `"top"`: The label is placed above the input field.
                * `"bottom"`: The label is placed below the input field.
        * **`activeLabel`**: `[str]` = `None` &rarr; The label to display when the prop value is True.
            * **Notes**: This attribute applies exclusively to `"toggle"` props.
        * **`placeholder`**: `[str]` = `None` &rarr; The placeholder text to display.
            * **Note**: This attribute applies to `"text"`, `"num"` (`"field"` variant), `"coordinate"` and `"selector"` props (only the `"dropdown"`, `"combobox"` and `"comboboxMulti"` variants). It is shown while nothing is selected, except for `"combobox"`, where it is used as the label of the input field.
        * **`direction`**: `[str]` = `"row"` &rarr; The layout direction of a coordinate prop's latitude/longitude fields.
            * **Accepted Values**:
                * `"row"`: The latitude and longitude fields are placed side by side.
                * `"column"`: The latitude and longitude fields are stacked vertically.
            * **Notes**:
                * This attribute applies exclusively to `"coordinate"` props.
                * For the `"latLngMap"` and `"latLngPath"` variants, only the latitude/longitude fields are affected; the map-toggle button always stays beside them.
        * **`defaultZoom`**: `[int | float]` = `None` &rarr; The initial zoom level of the popup map.
            * **Notes**:
                * Must be between `0` and `22`.
                * If left unspecified (i.e., `None`), a sensible default zoom level is used.
                * This attribute applies to the `"latLngMap"` and `"latLngPath"` variants of `"coordinate"` props.
        * **`minZoom`**: `[int | float]` = `None` &rarr; The minimum zoom level a user can zoom out to on the popup map.
            * **Notes**:
                * Must be between `0` and `22`.
                * This attribute applies to the `"latLngMap"` and `"latLngPath"` variants of `"coordinate"` props.
        * **`maxZoom`**: `[int | float]` = `None` &rarr; The maximum zoom level a user can zoom in to on the popup map.
            * **Notes**:
                * Must be between `0` and `22`.
                * This attribute applies to the `"latLngMap"` and `"latLngPath"` variants of `"coordinate"` props.
        * **`maxBounds`**: `[list[int | float]]` = `None` &rarr; The bounds the popup map can be panned within, as `[[west, south], [east, north]]`.
            * **Notes**:
                * Each corner is a `[longitude, latitude]` pair, where longitude is between `-180` and `180` and latitude is between `-90` and `90`.
                * `west` must be less than `east`, and `south` must be less than `north`.
                * If left unspecified (i.e., `None`), the popup map can be panned anywhere.
                * This attribute applies to the `"latLngMap"` and `"latLngPath"` variants of `"coordinate"` props.
        * **`pathColor`**: `[str]` = `None` &rarr; The color of the drawn path line.
            * **Notes**:
                * A valid color string (EG: "rgba(3, 170, 238, 0.5)")
                * If left unspecified (i.e., `None`), a default blue is used.
                * This attribute applies exclusively to the `"latLngPath"` variant of `"coordinate"` props.
        * **`pathWeight`**: `[int | float]` = `None` &rarr; The width of the drawn path line.
            * **Notes**:
                * Must be between `1` and `100`.
                * If left unspecified (i.e., `None`), a default width is used.
                * This attribute applies exclusively to the `"latLngPath"` variant of `"coordinate"` props.
        * **`maxValue`**: `[float | int]` = `None` &rarr; The maximum value for the prop.
            * **Note**: This attribute applies exclusively to `"num"` props.
        * **`minValue`**: `[float | int]` = `None` &rarr; The minimum value for the prop.
            * **Note**: This attribute applies exclusively to `"num"` props.
        * **`gradient`**: `[dict]` = `None` &rarr; The gradient to apply to the prop.
            * **Note**: See the `props_gradient` function for more information.
        * **`fallback`**: `[dict]` = `None` &rarr; The fallback dict for color and sizing props with missing or invalid values.
            * **Note**: See the `props_fallback` function for more information.
            * **Note**: This attribute applies to `"selector"`, `"num"`, `"text"`, and `"toggle"` props.
        * **`maxRows`**: `[int]` = `None` &rarr;
            * The maximum number of rows to show for a `"textarea"` variant.
            * **Note**: This attribute applies exclusively to `"text"` props.
        * **`minRows`**: `[int]` = `None` &rarr;
            * The minimum number of rows to show for a `"textarea"` variant.
            * **Note**: This attribute applies exclusively to `"text"` props.
        * **`rows`**: `[int]` = `None` &rarr;
            * The fixed number of rows to show for a `"textarea"` variant.
            * **Note**: This attribute applies exclusively to `"text"` props.
        * **`views`**: `[list[str]]` &rarr;
            * The available time units for the represented date and/or time.
            * **Default Value**:
                * When **`variant`** == `"date"`: `["year", "day"]`
                * When **`variant`** == `"time"`: `["hours", "minutes"]`
                * When **`variant`** == `"datetime"`: `["year", "day", "hours", "minutes"]`
            * **Accepted Values**:
                * When **`variant`** == `"date"`:
                    * `"year"`: The year view
                    * `"month"`: The month view
                    * `"day"`: The day view
                * When **`variant`** == `"time"`:
                    * `"hours"`: The hours view
                    * `"minutes"`: The minutes view
                    * `"seconds"`: The seconds view
                * When **`variant`** == `"datetime"`:
                    * `"year"`: The year view
                    * `"month"`: The month view
                    * `"day"`: The day view
                    * `"hours"`: The hours view
                    * `"minutes"`: The minutes view
                    * `"seconds"`: The seconds view
            * **Notes**:
                * The views will be presented in the order specified in the `views` array.
                * This attribute applies exclusively to `"date"` props.
        * **`defaultView`**: `[str]` = `None` &rarr; The view that the picker opens to.
            * **Accepted Values**: The same as the accepted values of **`views`** for the **`variant`**.
            * **Notes**:
                * Must be one of the available `views`, which are the default `views` of the **`variant`** if **`views`** is not provided.
                * If not provided, the picker opens to its default view, which is the `"day"` view for the `"date"` and `"datetime"` variants and the `"hours"` view for the `"time"` variant.
                * This attribute applies exclusively to `"date"` props.
        * **`dateOrder`**: `[str]` = `"mdy"` &rarr; The order of the month, day and year in which the date is displayed.
            * **Accepted Values**:
                * `"mdy"`: Month first, e.g. `07-09-2026`
                * `"dmy"`: Day first, e.g. `09-07-2026`
                * `"ymd"`: Year first, e.g. `2026-07-09`
            * **Notes**:
                * This only changes how the value is displayed. The value is always passed as described in **`variant`**.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`hour24`**: `[bool]` = `False` &rarr; Whether to display the time in a 24-hour clock. If `False`, a 12-hour clock with `AM`/`PM` is used.
            * **Notes**:
                * This only changes how the value is displayed and which hours the clock offers. The value is always passed as described in **`variant`**.
                * The seconds are only displayed if `"seconds"` is one of the available `views`.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`minDate`**: `[str]` = `None` &rarr; The earliest date that can be selected.
            * **Accepted Formats**: `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Only the date part is used, so any time part is ignored.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`maxDate`**: `[str]` = `None` &rarr; The latest date that can be selected.
            * **Accepted Formats**: `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Only the date part is used, so any time part is ignored.
                * Must not be earlier than `minDate`.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`minTime`**: `[str]` = `None` &rarr; The earliest time of day that can be selected.
            * **Accepted Formats**: `HH:MM:SS`, `HH:MM`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Only the time part is used, so any date part is ignored.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`maxTime`**: `[str]` = `None` &rarr; The latest time of day that can be selected.
            * **Accepted Formats**: `HH:MM:SS`, `HH:MM`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Only the time part is used, so any date part is ignored.
                * Must not be earlier than `minTime`.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`minDateTime`**: `[str]` = `None` &rarr; The earliest moment that can be selected, bound to a specific date.
            * **Accepted Formats**: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Unlike `minDate` and `minTime`, which limit the day and the time of day independently, this is a single cutoff. For example, with `"minDateTime": "2026-07-05T09:00:00"`, `08:00` on `2026-07-06` can be selected, whereas with `"minDate": "2026-07-05"` and `"minTime": "09:00"` it can not.
                * A time part is required, so a date-only string is rejected.
                * It combines with `minDate`, `maxDate`, `minTime` and `maxTime`, and only values that satisfy all of them can be selected.
                * This attribute applies exclusively to `"date"` props with the `"datetime"` variant.
        * **`maxDateTime`**: `[str]` = `None` &rarr; The latest moment that can be selected, bound to a specific date.
            * **Accepted Formats**: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * See `minDateTime` for how this differs from `maxDate` and `maxTime`.
                * A time part is required, so a date-only string is rejected.
                * Must not be earlier than `minDateTime`.
                * This attribute applies exclusively to `"date"` props with the `"datetime"` variant.
        * **`timezone`**: `[str]` = `None` &rarr; The timezone that the date and/or time of the prop belongs to.
            * **Accepted Values**:
                * `"system"`: The timezone of the user's browser
                * `"UTC"`: Coordinated Universal Time
                * Any [IANA timezone name], such as `"America/New_York"`
            * **Notes**:
                * Values are never converted between timezones. A value is the wall-clock date and/or time in this timezone, and it is displayed as it is stored.
                * The timezone defines what the present is, so it affects `disablePast` and `disableFuture` and the day highlighted as today.
                * The `minDate`, `maxDate`, `minTime`, `maxTime`, `minDateTime` and `maxDateTime` bounds are also read in this timezone.
                * A date and/or time that doesn't exist in this timezone, such as the hour skipped when clocks move forward, is displayed as the next valid one until a new value is selected.
                * If not provided (or `"system"`), the timezone of the user's browser is used.
                * This attribute applies exclusively to `"date"` props.
        * **`hoursStep`**: `[int]` = `None` &rarr; The step between the hours, e.g. `2` only allows even hours.
            * **Notes**:
                * Must divide `24` evenly (`1`, `2`, `3`, `4`, `6`, `8`, `12` or `24`).
                * A step only applies if the `"hours"` view is one of the available `views`.
                * Values that aren't a multiple of the step can't be selected.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`minutesStep`**: `[int]` = `None` &rarr; The step between the minutes, e.g. `15` only allows `00`, `15`, `30` and `45`.
            * **Notes**:
                * Must divide `60` evenly (`1`, `2`, `3`, `4`, `5`, `6`, `10`, `12`, `15`, `20`, `30` or `60`).
                * A step only applies if the `"minutes"` view is one of the available `views`.
                * Values that aren't a multiple of the step can't be selected.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`secondsStep`**: `[int]` = `None` &rarr; The step between the seconds, e.g. `30` only allows `00` and `30`.
            * **Notes**:
                * Must divide `60` evenly (`1`, `2`, `3`, `4`, `5`, `6`, `10`, `12`, `15`, `20`, `30` or `60`).
                * A step only applies if the `"seconds"` view is one of the available `views`.
                * Values that aren't a multiple of the step can't be selected.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`disabledTimes`**: `[list[list[str]]]` = `None` &rarr; Windows of the time of day that can't be selected, each one as a `[start, end]` pair.
            * **Accepted Formats**: `HH:MM:SS`, `HH:MM`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Example**: `[["12:00", "13:00"], ["22:00", "24:00"]]` disables lunch time and the last two hours of the day.
            * **Notes**:
                * The `start` is included in the window and the `end` is not, so `["12:00", "13:00"]` disables `12:00:00` to `12:59:59`.
                * The `end` of a window (and only the `end`) can also be `"24:00"` or `"24:00:00"`, which is the end of the day.
                * The `start` must be earlier than the `end`. A window can't go past midnight, so use two windows instead.
                * Only the time part is used, so any date part is ignored.
                * The windows can't disable the whole day.
                * An hour or a minute is disabled in its view only if all of it is disabled.
                * This attribute applies exclusively to `"date"` props with the `"time"` and `"datetime"` variants.
        * **`disabledDates`**: `[list[str]]` = `None` &rarr; Specific dates that can't be selected.
            * **Accepted Formats**: `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD HH:MM:SS`
            * **Notes**:
                * Only the date part is used, so any time part is ignored.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`disabledWeekdays`**: `[list[int | str]]` = `None` &rarr; Days of the week that can't be selected.
            * **Accepted Values**: A number from `0` (Sunday) to `6` (Saturday), a two-letter name (`"Su"`, `"Mo"`, `"Tu"`, `"We"`, `"Th"`, `"Fr"`, `"Sa"`), a three-letter name (`"Sun"`, `"Mon"`, ...) or a full name (`"Sunday"`, `"Monday"`, ...).
            * **Notes**:
                * Names are not case-sensitive, and the notations can be mixed in the same list.
                * Not all of the weekdays can be disabled, as that would leave nothing to select.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`disabledMonths`**: `[list[int | str]]` = `None` &rarr; Months of the year that can't be selected, in every year.
            * **Accepted Values**: A number from `1` (January) to `12` (December), a three-letter name (`"Jan"`, `"Feb"`, ...) or a full name (`"January"`, `"February"`, ...).
            * **Notes**:
                * Names are not case-sensitive, and the notations can be mixed in the same list.
                * Not all of the months can be disabled, as that would leave nothing to select.
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`disabledYears`**: `[list[int]]` = `None` &rarr; Years that can't be selected.
            * **Notes**:
                * This attribute applies exclusively to `"date"` props with the `"date"` and `"datetime"` variants.
        * **`disablePast`**: `[bool]` = `False` &rarr; Whether to prevent selecting values before the present.
            * **Notes**:
                * With the `"date"` variant, dates before today are disabled.
                * With the `"time"` variant, times before the current time of day are disabled.
                * With the `"datetime"` variant, moments before now are disabled.
                * The present is taken from the user's browser.
                * This attribute applies exclusively to `"date"` props.
        * **`disableFuture`**: `[bool]` = `False` &rarr; Whether to prevent selecting values after the present.
            * **Notes**:
                * With the `"date"` variant, dates after today are disabled.
                * With the `"time"` variant, times after the current time of day are disabled.
                * With the `"datetime"` variant, moments after now are disabled.
                * The present is taken from the user's browser.
                * This attribute applies exclusively to `"date"` props.
        * **`locale`**: `[str]` = `None` &rarr;
            * Format numeric values based on language and regional conventions.
            * **Notes**:
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.locale`.
                * This attribute applies exclusively to `"num"` props.
            * **See**: [Locale identifier][].
        * **`precision`**: `[int]` = `None` &rarr; The number of decimal places to display.
            * **Notes**:
                * Set the precision to `0` to attach an integer constraint.
                * If left unspecified (i.e., `None`):
                    * For `"num"` props, it will default to `settings.defaults.precision`.
                    * For `"coordinate"` props, it will default to `6` decimal places instead of `settings.defaults.precision`.
                * This attribute applies to `"num"` and `"coordinate"` props.
        * **`trailingZeros`**: `[bool]` = `None` &rarr; If `True`, trailing zeros will be displayed.
            * **Notes**:
                * This ensures that all precision digits are shown. For example: `1.5` &rarr; `1.500` when precision is `3`.
                * If left unspecified (i.e., `None`):
                    * For `"num"` props, it will default to `settings.defaults.trailingZeros`.
                    * For `"coordinate"` props, it will default to `True` instead of `settings.defaults.trailingZeros`.
                * This attribute applies to `"num"` and `"coordinate"` props.
        * **`fallbackValue`**: [str] = `None` &rarr; A value to show when the value is missing or invalid.
            * **Notes**:
                * This is only for display purposes as related to number formatting. It does not affect the actual value or any computations.
                    * For example, if the value passed is `None`, the fallback value will be displayed instead.
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.fallbackValue`.
                * This attribute applies exclusively to `"num"` props.
        * **`unit`**: `[str]` = `None` &rarr; The unit to use for the prop.
            * **Notes**:
                * If left unspecified (i.e., `None`):
                    * For `"num"` props, it will default to `settings.defaults.unit`.
                    * For `"coordinate"` props, no unit is shown (there is no coordinate-specific default, and `settings.defaults.unit` does not apply).
                * This attribute applies to `"num"` and `"coordinate"` props.
        * **`unitPlacement`**: `[str]` = `None` &rarr; The position of the `unit` symbol relative to the value.
            * **Accepted Values**:
                * `"after"`: The `unit` appears after the value.
                * `"afterWithSpace"`: The `unit` appears after the value, separated by a space.
                * `"before"`: The `unit` appears before the value.
                * `"beforeWithSpace"`: The unit is placed before the value, with a space in between.
            * **Notes**:
                * Only relevant when `unit` is also set.
                * If left unspecified (i.e., `None`):
                    * For `"num"` props, it will default to `settings.defaults.unitPlacement`.
                    * For `"coordinate"` props, it will default to `"after"` instead of `settings.defaults.unitPlacement`, since degree symbols are conventionally typeset directly against the number.
                * This attribute applies to `"num"` and `"coordinate"` props.
        * **`notation`**: `[str]` = `"standard"` &rarr; The formatting style of a numeric value.
            * **Accepted Values**:
                * `"standard"`: Plain number formatting
                * `"compact"`: Resembles the [metric prefix][] system
                * `"scientific"`: [Scientific notation][]
                * `"engineering"`: [Engineering notation][]
                * `"precision"`: Emulates the [Number.prototype.toPrecision][] method
            * **Notes**:
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.notation`.
                * This attribute applies exclusively to `"num"` props.
        * **`notationDisplay`**: `[str]` = `"e+"` | `"short"` &rarr; Further customize the formatting within the selected `notation`.
            * **Accepted Values**:
                * When **`notation`** == `"compact"`:
                    * `"short"`: Add symbols `K`, `M`, `B`, and `T` (in `"en-US"`) to denote thousands, millions, billions, and trillions, respectively.
                    * `"long"`: Present numeric values with the informal suffix words `thousand`, `million`, `billion`, and `trillion` (in `"en-US"`).
                * When **`notation`** == `"scientific"`, `"engineering"` or `"precision"`:
                    * `"e"`: Exponent symbol in lowercase as per the chosen `locale` identifier
                    * `"e+"`: Similar to `"e"`, but with a plus sign for positive exponents.
                    * `"E"`: Exponent symbol in uppercase as per the chosen `locale` identifier
                    * `"E+"`: Similar to `"E"`, but with a plus sign for positive exponents.
                    * `"x10^"`: Formal scientific notation representation
                    * `"x10^+"`: Similar to `"x10^"`, with a plus sign for positive exponents.
                * When **`notation`** == `"standard"`:
                    * No `notationDisplay` option is allowed for a `"standard"` notation
            * **Notes**:
                * No `notationDisplay` option is provided for a `"standard"` notation
                * The options `"short"` and `"long"` are only provided for the `"compact"` notation
                * The options `"e"`, `"e+"`, `"E"`, `"E+"`, `"x10^"`, and `"x10^+"` are provided for the `"scientific"`, `"engineering"` and `"precision"` notations
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.notationDisplay`.
                * This attribute applies exclusively to `"num"` props.
        * **`legendPrecision`**: `[int]` = `None` &rarr;
            * The number of decimal places to display in the Map Legend.
            * **Notes**:
                * Set the precision to `0` to attach an integer constraint.
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.legendPrecision`.
                * This attribute applies exclusively to `"num"` props.
        * **`legendNotation`**: `[str]` = `"standard"` &rarr; The formatting style of a numeric value.
            * **Accepted Values**:
                * `"standard"`: Plain number formatting
                * `"compact"`: Resembles the [metric prefix][] system
                * `"scientific"`: [Scientific notation][]
                * `"engineering"`: [Engineering notation][]
                * `"precision"`: Emulates the [Number.prototype.toPrecision][] method
            * **Notes**:
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.legendNotation`.
                * This attribute applies exclusively to `"num"` props.
        * **`legendNotationDisplay`**: `[str]` = `"e+"` | `"short"` &rarr; Further customize the formatting within the selected `legendNotation`.
            * **Accepted Values**:
                * `"short"`: Add symbols `K`, `M`, `B`, and `T` (in `"en-US"`) to denote thousands, millions, billions, and trillions, respectively.
                * `"long"`: Present numeric values with the informal suffix words `thousand`, `million`, `billion`, and `trillion` (in `"en-US"`).
                * `"e"`: Exponent symbol in lowercase as per the chosen `locale` identifier
                * `"e+"`: Similar to `"e"`, but with a plus sign for positive exponents.
                * `"E"`: Exponent symbol in uppercase as per the chosen `locale` identifier
                * `"E+"`: Similar to `"E"`, but with a plus sign for positive exponents.
                * `"x10^"`: Formal scientific notation representation
                * `"x10^+"`: Similar to `"x10^"`, with a plus sign for positive exponents.
            * **Notes**:
                * No `legendNotationDisplay` option is provided for a `"standard"` legend notation
                * The options `"short"` and `"long"` are only provided for the `"compact"` legend notation
                * The options `"e"`, `"e+"`, `"E"`, `"E+"`, `"x10^"`, and `"x10^+"` are provided for the `"scientific"`, `"engineering"` and `"precision"` notations
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.legendNotationDisplay`.
                * This attribute applies exclusively to `"num"` props.
        * **`legendMinLabel`**: `[str]` = `None` &rarr;
            * A custom and descriptive label in the Map Legend used to identify the lowest data point.
            * **Notes**:
                * Takes precedence over other formatting, except when used in a node cluster and the `cave_utils.api.maps.group` attribute is `True`. In this case, the min value within the node cluster is displayed.
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.legendMinLabel`.
                * This attribute applies exclusively to `"num"` props.
        * **`legendMaxLabel`**: `[str]` = `None` &rarr;
            * A custom and descriptive label in the Map Legend used to identify the highest data point.
            * **Notes**:
                * Takes precedence over other formatting, except when used in a node cluster and the `cave_utils.api.maps.group` attribute is `True`. In this case, the max value within the node cluster is displayed.
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.legendMaxLabel`.
                * This attribute applies exclusively to `"num"` props.
        * **`icon`**: `[str]` = `None` &rarr; The icon to use for the prop.
            * **Notes**:
                * It must be a valid icon name from the [react-icons][] bundle, preceded by the abbreviated name of the icon library source.
                * Applies to `"head"` props (all variants), the `icon` variants of various other props, and also `toggle`, `button`, and `selector` props.
        * **`activeIcon`**: `[str]` = `None` &rarr; The icon to use for the prop when it is active.
            * **Notes**: Applies to the `toggle` and `selector` props.
        * **`startIcon`**: `[str]` = `None` &rarr; The icon to display at the start of the prop.
            * **Notes**: Applies to the `button` prop and offers a way to add an icon to the left side of the button.
        * **`endIcon`**: `[str]` = `None` &rarr; The icon to display at the end of the prop.
            * **Notes**: Applies to the `button` prop and offers a way to add an icon to the right side of the button.
        * **`color`**: `[str]` = `None` &rarr; The color to use for the prop.
            * **Notes**: Applies to `"head"` props (all variants), the `icon` variants of various other props, and also `toggle`, `button`, and `selector` props.
        * **`activeColor`**: `[str]` = `None` &rarr; The color to use for the prop when it is active.
            * **Notes**: Applies to the `toggle` and `selector` props.
        * **`size`**: `[str]` = `None` &rarr; The size of the icon in the prop.
            * **Notes**: Applies to `"head"` props (all variants), the `icon` variants of various other props, and also `toggle`, `button`, and `selector` props.
        * **`activeSize`**: `[str]` = `None` &rarr; The size of the icon in the prop when it is active.
            * **Notes**: Applies to the `toggle` and `selector` props.
        * **`placement`**: `[str]` = `None` &rarr; The placement of the prop.
            * **Accepted Values**:
                * `"start"`: The prop is placed at the start of the container.
                * `"end"`: The prop is placed at the end of the container.
                * `"top"`: The prop is placed at the top of the container.
                * `"bottom"`: The prop is placed at the bottom of the container.
                * `"center"`: The prop is placed at the center of the container.
        * **`fullWidth`**: `[bool]` = `None` &rarr; Whether or not the prop should take the full width of the container.
            * **Notes**:
                * For `media` props, `fullWidth: True` expresses the same as `scaleMode: "fitWidth"`.
                * If both `fullWidth` and `scaleMode` are used, `scaleMode` takes precedence and a warning is logged.
                * `"audio"` props only support `fullWidth`: they have a fixed height, so `scaleMode` does not apply.
        * **`url`**: `[str]` = `None` &rarr; The URL to navigate to when the button is clicked.
            * **Notes**: Applies to `"button"` props.
        * **`suppressCommand`**: `[bool]` = `False` &rarr;
            * If `True` and `url` is also set, clicking the button only navigates to `url`; the paired `apiCommand` (if any) is not triggered.
            * **Notes**:
                * Applies to `"button"` props.
                * Has no effect unless both `url` and `apiCommand` are set. Otherwise, `apiCommand` (if any) always triggers on click.
        * **`scaleMode`**: `[str]` = `None` &rarr; The scale mode to use for the prop.
            * **Accepted Values**:
                * `"fitWidth"`: The prop will scale to fit the width of its container. Its height follows the media's aspect ratio.
                * `"fitHeight"`: The prop will scale to fit the height of its container. Its width follows the media's aspect ratio.
                * `"fitContainer"`: The prop will scale to cover the width and height of its container without cropping. The side that does not bind expands.
            * **Notes**:
                * Applies only to `media` props with a `variant` of `picture` or `video`.
                * `scaleMode` takes precedence over `fullWidth`.
        * **`propStyle`**: `[dict]` = `None` &rarr; A dictionary of css styles to apply to the prop.
            * **Note**: This will not be validated as part of the API spec, so use with caution.
        * **`readOnly`**: `[bool]` = `False` &rarr; Whether or not the prop is read-only.
            * **Notes**:
                - Only applies to `"text"`, `"date"` and `"num"` props (`"field"` variant), and to `"selector"` props `"selector"` props (only the `"combobox"`, `"comboboxMulti"` and `"dualList"` variants).
                - Essentially operates an enabled without making the prop darkened.
        * **`marks`**: `[dict[str, dict[str, str]]]` = `None` &rarr; A dictionary of marks to display on the slider.
            * **Notes**:
                - Only applies to `"num"` props with the `"incslider"` variant.
                - Contains key-value pairs for each mark, where the key is the mark value and the value is a dictionary of properties for the mark (e.g., label, color).
                # TODO: Add more details and validation for the `marks` dictionary.
        * **`draggable`**: `[bool]` = `None` &rarr; **Deprecated**, will be removed in `4.0.0`, in favor of `quickView`.
            * If `True`, the prop will be rendered within the draggable global outputs pad.
            * **Notes**:
                * The prop's `variant` is enforced to `"iconCompact"` to accommodate it within the draggable pad.
                * This attribute applies exclusively to `"num"` props defined within `cave_utils.api.globalOutputs`.
        * **`quickView`**: `[bool]` = `None` &rarr;
            * If `True`, the prop will be rendered within the global outputs quick-view display: the draggable pad, or, if the user has docked global outputs, a card within the persistent status bar carousel.
            * **Notes**:
                * The prop's `variant` is enforced to `"iconCompact"` or `"iconCompactAlt"` (depending on whether global outputs are docked) to accommodate it within either display.
                * This attribute applies exclusively to `"num"` props defined within `cave_utils.api.globalOutputs`.
                * `draggable` is still accepted as a deprecated alias of this attribute.
        * **`allowNone`**: `[bool]` = `False` &rarr;
            * Whether or not to allow `None` as a valid value for the prop. This is primarily used to help when validating `values` and `valueLists`.
            * **Notes**:
                * If `True`, `None` will be a valid value for the prop.
                    * `None` values will be treated differently in the front end
                        * For map display purposes: `None` values will be shown as a different color or ignored.
                            * See `nullColor` in: `/cave_utils/cave_utils/api/maps.html#colorByOptions`
                        * For prop purposes: `None` values will be left blank.
                * If `False`, `None` will not be a valid value for the prop.
                * This attribute applies to all props except `"head"` props.
        * **`marqueeLabel`**: `[bool]` = `True` &rarr; Whether to scroll (marquee) a label that overflows its container.
            * **Notes**:
                * If `True`, an overflowing label will scroll horizontally instead of being truncated.
                * This attribute applies exclusively to `"num"` props with the `"field"` variant (or no variant).
        * **`spinner`**: `[str | bool]` = `"right"` &rarr; Controls the visibility and placement of increment/decrement spinner buttons.
            * **Accepted Values**:
                * `"left"`: Displays a decrement button on the left side of the input.
                * `"right"` | `True`: Displays an increment button on the right side of the input.
                * `"leftAndRight"`: Displays a decrement button on the left and an increment button on the right, centering the input value between them.
                * `False`: Hides the spinner control entirely.
            * **Notes**:
                * If `None`, the default spinner behavior is used.
                * This attribute applies exclusively to `"num"` props with the `"field"` variant (or no variant).
        * **`smallStep`**: `[float | int]` = `None` &rarr; Defines a finer-grained increment step for precise adjustments (typically triggered via a modifier key such as Alt).
            * **Notes**:
                * Default: a decimal value derived from `precision` (i.e. `10^(-precision)`); if unavailable, falls back to `0.1`.
                    * Example: if `precision` is `3`, the default `smallStep` is `0.001`.
                * This attribute applies to `"num"` props with the `"field"` or `"slider"` variant.
        * **`step`**: `[float | int]` = `None` &rarr; Defines the default increment/decrement step when the value changes (e.g. via arrow keys, spinner buttons, or drag interactions).
            * **Notes**:
                * Default: `1`.
                * This attribute applies to `"num"` props with the `"field"` or `"slider"` variant.
        * **`largeStep`**: `[float | int]` = `None` &rarr; Defines a larger increment step for faster value changes (typically triggered via a modifier key such as Shift).
            * **Notes**:
                * Default: `10`.
                * This attribute applies to `"num"` props with the `"field"` or `"slider"` variant.
        * **`hideKeyboardToggle`**: `[bool]` = `None` &rarr; Whether to hide the on-screen keyboard toggle button.
            * **Notes**:
                * This attribute applies exclusively to `"num"` props with the `"field"` variant (or no variant).
        * **`scale`**: `[str]` = `None` &rarr; The scale used for the slider's non-linear thumb-position mapping.
            * **Accepted Values**:
                * `"linear"`: Position the thumb linearly across `[minValue, maxValue]`
                * `"log"`: Position the thumb logarithmically, giving finer control near `minValue`
                * `"pow"`: Position the thumb using `scaleParams.exponent` as the power
                * `"exp"`: Position the thumb exponentially, giving finer control near `maxValue`
            * **Notes**:
                * `scale`/`scaleParams` only reshape how drag distance maps to the thumb's position; `minValue`, `maxValue`, and the prop's value remain the same real-world quantity regardless of scale.
                * This attribute applies exclusively to `"num"` props with the `"slider"` variant.
                * `minValue` and `maxValue` must both be greater than `0` when using an exponential scale.
        * **`scaleParams`**: `[dict]` = `None` &rarr; The parameters for the scale.
            * **Notes**:
                * See `props_slider_scaleParams` for more information.
                * This attribute applies exclusively to `"num"` props with the `"slider"` variant.

        [react-icons]: https://react-icons.github.io/react-icons/search
        [metric prefix]: https://en.wikipedia.org/wiki/Metric_prefix
        [Scientific notation]: https://en.wikipedia.org/wiki/Scientific_notation
        [Engineering notation]: https://en.wikipedia.org/wiki/Engineering_notation
        [IANA timezone name]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        [Number.prototype.toPrecision]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toPrecision
        """
        passed_values = {k: v for k, v in locals().items() if (v is not None) and k != "kwargs"}
        required_fields = ["name", "type"]
        optional_fields = [
            "subtitle",
            "help",
            "helperText",
            "variant",
            "display",
            "container",
            "propStyle",
            "fullWidth",
            "placement",
            "labelPlacement",
        ]
        if type == "head":
            # `icon`/`color`/`size` apply to all `head` variants (`column`, `row`, and the
            # deprecated `icon`/`iconRow` aliases), which all render identically.
            optional_fields += ["icon", "color", "size"]
        else:
            optional_fields += ["enabled", "apiCommand", "apiCommandKeys", "allowNone"]

        if type == "text":
            optional_fields += [
                "minRows",
                "maxRows",
                "rows",
                "label",
                "placeholder",
                "options",
                "readOnly",
                "fallback",
            ]
        elif type == "num":
            optional_fields += ["color"]
            if variant == "slider":
                required_fields += ["maxValue", "minValue"]
                optional_fields += ["smallStep", "step", "largeStep", "scale", "scaleParams"]
            elif variant == "incslider":
                required_fields += ["valueOptions"]
                optional_fields += ["marks"]
            else:
                optional_fields += ["maxValue", "minValue"]
                if variant is None or variant == "field":
                    optional_fields += [
                        "label",
                        "placeholder",
                        "marqueeLabel",
                        "spinner",
                        "smallStep",
                        "step",
                        "largeStep",
                        "hideKeyboardToggle",
                        "readOnly",
                    ]
            if variant == "icon" or variant == "iconCompact" or variant == "iconCompactAlt":
                required_fields += ["icon"]
                optional_fields += ["color", "size"]
            if notationDisplay:
                required_fields += ["notation"]
            if legendNotationDisplay:
                required_fields += ["legendNotation"]
            optional_fields += [
                "unit",
                "notation",
                "precision",
                "notationDisplay",
                "legendNotation",
                "legendPrecision",
                "legendNotationDisplay",
                "legendMinLabel",
                "legendMaxLabel",
                "trailingZeros",
                "unitPlacement",
                "draggable",
                "quickView",
                "gradient",
                "fallback",
            ]
        elif type == "selector":
            required_fields += ["options"]
            optional_fields += [
                "color",
                "activeColor",
                "size",
                "activeSize",
                "icon",
                "activeIcon",
                "fallback",
            ]
            # `dropdown` is the default `variant` for `selector` props
            if variant in (None, "dropdown", "combobox", "comboboxMulti"):
                optional_fields += ["placeholder"]
            if variant == "comboboxMulti":
                optional_fields += ["numVisibleTags"]
            if variant in ("combobox", "comboboxMulti", "dualList"):
                optional_fields += ["readOnly"]
            if variant == "dualList":
                optional_fields += ["availableTitle", "selectedTitle", "height"]
        elif type == "date":
            optional_fields += [
                "views",
                "defaultView",
                "label",
                "readOnly",
                "timezone",
                "disablePast",
                "disableFuture",
            ]
            if variant in (None, "date", "datetime"):
                optional_fields += [
                    "dateOrder",
                    "minDate",
                    "maxDate",
                    "disabledDates",
                    "disabledWeekdays",
                    "disabledMonths",
                    "disabledYears",
                ]
            if variant in ("time", "datetime"):
                optional_fields += [
                    "hour24",
                    "minTime",
                    "maxTime",
                    "disabledTimes",
                    "hoursStep",
                    "minutesStep",
                    "secondsStep",
                ]
            if variant == "datetime":
                optional_fields += ["minDateTime", "maxDateTime"]
        elif type == "coordinate":
            optional_fields += [
                "placeholder",
                "precision",
                "trailingZeros",
                "unit",
                "unitPlacement",
                "direction",
            ]
            if variant in ("latLngInput", "latLngMap", "latLngPath"):
                optional_fields += ["defaultZoom", "minZoom", "maxZoom", "maxBounds"]
            if variant == "latLngPath":
                optional_fields += ["pathColor", "pathWeight"]
        elif type == "toggle":
            optional_fields += [
                "options",
                "icon",
                "color",
                "size",
                "label",
                "activeColor",
                "activeSize",
                "activeLabel",
                "activeIcon",
                "fallback",
            ]
        elif type == "button":
            optional_fields += [
                "icon",
                "color",
                "size",
                "startIcon",
                "endIcon",
                "url",
                "suppressCommand",
            ]
        elif type == "media":
            required_fields += ["variant"]
            optional_fields = [i for i in optional_fields if i != "variant"]
            if variant in ["picture", "video"]:
                optional_fields += ["scaleMode"]

        missing_required = pamda.difference(required_fields, list(passed_values.keys()))
        if len(missing_required) > 0:
            raise Exception(f"Missing required fields: {str(missing_required)}")

        for k, v in passed_values.items():
            if k not in required_fields + optional_fields:
                kwargs[k] = v
        notationDisplay_options_dict = {
            "compact": ["short", "long"],
            "scientific": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "engineering": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "precision": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "standard": [],
        }
        notation = passed_values.get("notation", "standard")
        legendNotation = passed_values.get("legendNotation", "standard")
        view_options_dict = {
            "date": ["year", "month", "day"],
            "time": ["hours", "minutes", "seconds"],
            "datetime": ["year", "month", "day", "hours", "minutes", "seconds"],
        }
        variant = passed_values.get("variant", None)
        # `date` is the default `variant` of `date` props
        date_variant = variant or "date"
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "type": [
                    "head",
                    "num",
                    "toggle",
                    "button",
                    "text",
                    "selector",
                    "date",
                    "media",
                    "coordinate",
                ],
                "container": ["vertical", "horizontal", "titled", "untitled", "none"],
                "direction": ["row", "column"],
                "views": view_options_dict.get(date_variant, []),
                "defaultView": view_options_dict.get(date_variant, []),
                "dateOrder": ["mdy", "dmy", "ymd"],
                "unitPlacement": ["after", "afterWithSpace", "before", "beforeWithSpace"],
                "notation": ["standard", "compact", "scientific", "engineering", "precision"],
                "notationDisplay": notationDisplay_options_dict.get(notation, []),
                "legendNotation": ["standard", "compact", "scientific", "engineering", "precision"],
                "legendNotationDisplay": notationDisplay_options_dict.get(legendNotation, []),
                "placement": [
                    "topLeft",
                    "topCenter",
                    "topRight",
                    "left",
                    "center",
                    "right",
                    "bottomLeft",
                    "bottomCenter",
                    "bottomRight",
                ],
                "spinner": [True, False, "left", "right", "leftAndRight"],
                "scale": ["linear", "log", "pow", "exp"],
                "variant": {
                    "head": ["column", "row", "icon", "iconRow"],
                    "text": ["single", "textarea"],
                    "num": [
                        "field",
                        "slider",
                        "icon",
                        "iconCompact",
                        "iconCompactAlt",
                        "incslider",
                    ],
                    "selector": [
                        "dropdown",
                        "dualList",
                        "checkbox",
                        "radio",
                        "combobox",
                        "comboboxMulti",
                        "hstepper",
                        "vstepper",
                        "hradio",
                        "hcheckbox",
                        "nested",
                    ],
                    "date": ["date", "time", "datetime"],
                    "media": ["picture", "video", "audio"],
                    "coordinate": ["latLngInput", "latLngMap", "latLngPath"],
                    "toggle": ["switch", "button", "checkbox"],
                    "button": ["outlined", "text", "icon", "filled"],
                }.get(type, []),
            },
        }

    def __extend_spec__(self, **kwargs):
        if (
            self.data.get("type") == "media"
            and self.data.get("fullWidth") is True
            and self.data.get("scaleMode") is not None
        ):
            self.__warn__(
                msg="`scaleMode` takes precedence over `fullWidth` for `media` props, so `fullWidth` has no effect when both are used",
                path=["fullWidth"],
            )
        if self.data.get("type") == "selector":
            CustomKeyValidator(
                data=self.data.get("options", {}),
                log=self.log,
                prepend_path=["options"],
                validator=props_options,
                variant=self.data.get("variant"),
                **kwargs,
            )
        if self.data.get("gradient"):
            props_gradient(
                data=self.data.get("gradient"), log=self.log, prepend_path=["gradient"], **kwargs
            )
        if self.data.get("scale") is not None or self.data.get("scaleParams") is not None:
            props_slider_scaleParams(
                data=self.data.get("scaleParams", {}),
                log=self.log,
                prepend_path=["scaleParams"],
                slider_scale_type=self.data.get("scale"),
            )
            min_value = self.data.get("minValue")
            max_value = self.data.get("maxValue")
            if self.data.get("scale") == "exp":
                if min_value is not None and min_value <= 0:
                    self.__error__(msg="`minValue` must be greater than 0 for an exponential scale")
                if max_value is not None and max_value <= 0:
                    self.__error__(msg="`maxValue` must be greater than 0 for an exponential scale")
        if self.data.get("fallback"):
            props_fallback(
                data=self.data.get("fallback"), log=self.log, prepend_path=["fallback"], **kwargs
            )
        if self.data.get("color"):
            self.__check_color_string_valid__(color_string=self.data.get("color"))
        if self.data.get("activeColor"):
            self.__check_color_string_valid__(color_string=self.data.get("activeColor"))
        if self.data.get("size"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("size"))
        if self.data.get("activeSize"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("activeSize"))
        if self.data.get("type") == "date":
            if self.data.get("timezone") is not None:
                self.__check_timezone_valid__(self.data.get("timezone"), prepend_path=["timezone"])
            available_views = self.data.get("views") or DATE_DEFAULT_VIEWS.get(
                self.data.get("variant", "date"), []
            )
            default_view = self.data.get("defaultView")
            if default_view is not None:
                # Only checked when valid, as an unaccepted value is already reported
                if default_view in DATE_VIEW_NAMES and default_view not in available_views:
                    self.__error__(
                        msg=f"`defaultView = {default_view}` but it should be one of the available `views`: {available_views}",
                        path=["defaultView"],
                    )
            for unit, limit in DATE_TIME_STEP_LIMITS.items():
                step = self.data.get(f"{unit}Step")
                if step is None:
                    continue
                if step < 1 or limit % step != 0:
                    self.__error__(
                        msg=f"`{unit}Step = {step}` but it should be a positive integer that divides {limit} evenly",
                        path=[f"{unit}Step"],
                    )
                elif step > 1 and unit not in available_views:
                    self.__warn__(
                        msg=f"`{unit}Step` has no effect as the `{unit}` view is not one of the available `views`",
                        path=[f"{unit}Step"],
                    )
            for key, names, first, label in (
                ("disabledWeekdays", DATE_WEEKDAY_NAMES, 0, "weekday"),
                ("disabledMonths", DATE_MONTH_NAMES, 1, "month"),
            ):
                entries = self.data.get(key) or []
                indexes = set()
                for i, entry in enumerate(entries):
                    index = self.__to_calendar_index__(entry, names, first)
                    if index is None:
                        self.__error__(
                            msg=f"`{key}` has `{entry}` but it should be a {label} number from {first} to {first + len(names) - 1} or a {label} name",
                            path=[key, i],
                        )
                    else:
                        indexes.add(index)
                if len(indexes) == len(names):
                    self.__error__(msg=f"`{key}` disables every {label}", path=[key])
            for i, entry in enumerate(self.data.get("disabledDates") or []):
                if self.__parse_date_bound__(entry, DATE_DISABLED_DATE_FORMATS) is None:
                    self.__error__(
                        msg=f"`disabledDates` has `{entry}` but it should be in one of the accepted formats: {', '.join(DATE_DISABLED_DATE_FORMAT_NAMES)}",
                        path=["disabledDates", i],
                    )
            windows = []
            for i, window in enumerate(self.data.get("disabledTimes") or []):
                if len(window) != 2:
                    self.__error__(
                        msg=f"`disabledTimes` has a window of {len(window)} times but it should be a `[start, end]` pair",
                        path=["disabledTimes", i],
                    )
                    continue
                start = self.__to_seconds_of_day__(window[0])
                end = self.__to_seconds_of_day__(window[1], is_end=True)
                for j, (boundary, seconds) in enumerate(zip(window, (start, end))):
                    if seconds is None:
                        self.__error__(
                            msg=f"`disabledTimes` has `{boundary}` but it should be in one of the accepted formats: {', '.join(DATE_TIME_OF_DAY_FORMAT_NAMES)}"
                            + (" (or `24:00` for an end)" if j == 1 else ""),
                            path=["disabledTimes", i, j],
                        )
                if start is None or end is None:
                    continue
                if start >= end:
                    self.__error__(
                        msg=f"`disabledTimes` has the window `{window[0]}` to `{window[1]}` but the start must be earlier than the end",
                        path=["disabledTimes", i],
                    )
                else:
                    windows.append((start, end))
            covered_until = 0
            for start, end in sorted(windows):
                if start > covered_until:
                    break
                covered_until = max(covered_until, end)
            if covered_until == SECONDS_PER_DAY:
                self.__error__(msg="`disabledTimes` disables the whole day", path=["disabledTimes"])
            for lower, upper, part, formats, format_names in (
                ("minDate", "maxDate", "date", DATE_BOUND_FORMATS, DATE_BOUND_FORMAT_NAMES),
                ("minTime", "maxTime", "time", DATE_BOUND_FORMATS, DATE_BOUND_FORMAT_NAMES),
                (
                    "minDateTime",
                    "maxDateTime",
                    None,
                    DATETIME_BOUND_FORMATS,
                    DATETIME_BOUND_FORMAT_NAMES,
                ),
            ):
                parsed = {}
                for key in (lower, upper):
                    bound = self.data.get(key)
                    if bound is None:
                        continue
                    parsed[key] = self.__parse_date_bound__(bound, formats)
                    if parsed[key] is None:
                        self.__error__(
                            msg=f"`{key} = {bound}` but it should be in one of the accepted formats: {', '.join(format_names)}",
                            path=[key],
                        )
                if len(parsed) == 2 and None not in parsed.values():
                    low, high = (
                        (getattr(parsed[k], part)() if part else parsed[k]) for k in (lower, upper)
                    )
                    if low > high:
                        self.__error__(
                            msg=f"`{lower}` must not be later than `{upper}`",
                            path=[lower],
                        )
        if self.data.get("type") == "coordinate":
            variant = self.data.get("variant", "latLngMap")
            if variant in ("latLngInput", "latLngMap", "latLngPath"):
                for field in ("defaultZoom", "minZoom", "maxZoom"):
                    value = self.data.get(field)
                    if value is not None and (value < 0 or value > 22):
                        self.__error__(msg=f"`{field} = {value}` but it should be between 0 and 22")
                max_bounds = self.data.get("maxBounds")
                if max_bounds is not None:
                    is_bounds_shape = (
                        isinstance(max_bounds, list)
                        and len(max_bounds) == 2
                        and all(
                            isinstance(corner, list)
                            and len(corner) == 2
                            and all(
                                isinstance(num, (int, float)) and not isinstance(num, bool)
                                for num in corner
                            )
                            for corner in max_bounds
                        )
                    )
                    if not is_bounds_shape:
                        self.__error__(
                            msg=f"`maxBounds = {max_bounds}` but it should be `[[west, south], [east, north]]`"
                        )
                    else:
                        (west, south), (east, north) = max_bounds
                        for lng in (west, east):
                            if lng < -180 or lng > 180:
                                self.__error__(
                                    msg=f"`maxBounds` longitude `{lng}` but it should be between -180 and 180"
                                )
                        for lat in (south, north):
                            if lat < -90 or lat > 90:
                                self.__error__(
                                    msg=f"`maxBounds` latitude `{lat}` but it should be between -90 and 90"
                                )
                        if west >= east:
                            self.__error__(
                                msg=f"`maxBounds` west `{west}` must be less than east `{east}`"
                            )
                        if south >= north:
                            self.__error__(
                                msg=f"`maxBounds` south `{south}` must be less than north `{north}`"
                            )
            if variant == "latLngPath":
                if self.data.get("pathColor"):
                    self.__check_color_string_valid__(color_string=self.data.get("pathColor"))
                path_weight = self.data.get("pathWeight")
                if path_weight is not None and (path_weight < 1 or path_weight > 100):
                    self.__error__(
                        msg=f"`pathWeight = {path_weight}` but it should be between 1 and 100"
                    )


@type_enforced.Enforcer
class props_options(ApiValidator):
    @staticmethod
    def spec(
        name: str,
        activeName: str | None = None,
        path: list[str] | None = None,
        help: str | None = None,
        helperText: str | None = None,
        color: str | None = None,
        activeColor: str | None = None,
        size: str | None = None,
        activeSize: str | None = None,
        icon: str | None = None,
        activeIcon: str | None = None,
        enabled: bool | None = True,
        **kwargs,
    ):
        """
        Arguments:

        * **`name`**: `[str]` &rarr; The name of the option.
        * **`activeName`**: `[str]` = `None` &rarr; The name of the option when it is active.
            * **Note**: If not set, the `name` will be used regardless of the active state.
        * **`path`**: `[list[str]]` = `None` &rarr; The path to an option.
            * **Notes**:
                * If `None`, the option will not be selectable
                * This attribute applies exclusively to `"nested"` props
        * **`help`**: `[str]` = `None` &rarr; The help text to display for this option.
            * **Note**: This can be raw text or markdown formatted text.
        * **`helperText`**: `[str]` = `None` &rarr; The helper text to display for this option.
        * **`color`**: `[str]` = `None` &rarr; The color to use for this option.
            * **Note**: A valid color string (EG: "RGBA(0,0,0,1)")
        * **`activeColor`**: `[str]` = `None` &rarr; The color to use for this option when it is active.
            * **Note**: If not set the `color` will be used regardless of the active state.
        * **`size`**: `[str]` = `None` &rarr; The size to use for this option.
            * **Note**: A valid size string (EG: "5px")
        * **`activeSize`**: `[str]` = `None` &rarr; The size to use for this option when it is active.
            * **Note**: If not set the `size` will be used regardless of the active state.
        * **`icon`**: `[str]` = `None` &rarr; The icon to use for this option.
        * **`activeIcon`**: `[str]` = `None` &rarr; The icon to use for this option when it is active.
            * **Note**: If not set the `icon` will be used regardless of the active state.
        * **`enabled`**: `[bool]` = `True` &rarr; Whether or not the option will be enabled.
        """
        variant = kwargs.get("variant")
        kwargs = {k: v for k, v in kwargs.items() if k != "variant"}
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
        if self.data.get("color"):
            self.__check_color_string_valid__(color_string=self.data.get("color"))
        if self.data.get("activeColor"):
            self.__check_color_string_valid__(color_string=self.data.get("activeColor"))
        if self.data.get("size"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("size"))
        if self.data.get("activeSize"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("activeSize"))


@type_enforced.Enforcer
class props_fallback(ApiValidator):
    @staticmethod
    def spec(
        name: str | None = None,
        color: str | None = None,
        size: str | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`name`**: `[str]` = `None` &rarr; The name of the fallback.
        * **`color`**: `[str]` = `None` &rarr; The color to use for this fallback.
            * **Note**: A valid color string (EG: "RGBA(0,0,0,1)")
        * **`size`**: `[str]` = `None` &rarr; The size to use for this fallback.
            * **Note**: A valid size string (EG: "5px")
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        if self.data.get("color"):
            self.__check_color_string_valid__(color_string=self.data.get("color"))
        if self.data.get("size"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("size"))


@type_enforced.Enforcer
class props_gradient(ApiValidator):
    @staticmethod
    def spec(
        scale: str | None = None,
        scaleParams: dict | None = None,
        notation: str | None = None,
        notationDisplay: str | None = None,
        precision: int | None = None,
        data: list | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`scale`**: `[str]` = `None` &rarr; The scale to use for the gradient.
            * **Accepted Values**:
                * `"linear"`: A linear gradient
                * `"log"`: A logarithmic gradient
                * `"pow"`: A power gradient
                * `"step"`: A step gradient
        * **`scaleParams`**: `[dict]` = `None` &rarr; The parameters for the scale.
            * **Note**: See `props_gradient_scaleParams` for more information.
        * **`notation`**: `[str]` = `None` &rarr; The notation to use for the gradient.
            * **Accepted Values**:
                * `"standard"`: Plain number formatting
                * `"compact"`: Resembles the [metric prefix][] system
                * `"scientific"`: [Scientific notation][]
                * `"engineering"`: [Engineering notation][]
                * `"precision"`: Emulates the [Number.prototype.toPrecision][] method
        * **`notationDisplay`**: `[str]` = `"e+"` | `"short"` &rarr; Further customize the formatting within the selected `notation` when shown next to the gradient.
            * **Accepted Values**:
                * When **`notation`** == `"compact"`:
                    * `"short"`: Add symbols `K`, `M`, `B`, and `T` (in `"en-US"`) to denote thousands, millions, billions, and trillions, respectively.
                    * `"long"`: Present numeric values with the informal suffix words `thousand`, `million`, `billion`, and `trillion` (in `"en-US"`).
                * When **`notation`** == `"scientific"`, `"engineering"` or `"precision"`:
                    * `"e"`: Exponent symbol in lowercase as per the chosen `locale` identifier
                    * `"e+"`: Similar to `"e"`, but with a plus sign for positive exponents.
                    * `"E"`: Exponent symbol in uppercase as per the chosen `locale` identifier
                    * `"E+"`: Similar to `"E"`, but with a plus sign for positive exponents.
                    * `"x10^"`: Formal scientific notation representation
                    * `"x10^+"`: Similar to `"x10^"`, with a plus sign for positive exponents.
                * When **`notation`** == `"standard"`:
                    * No `notationDisplay` option is allowed for a `"standard"` notation
            * **Notes**:
                * If left unspecified (i.e., `None`), it will default to `settings.defaults.notationDisplay`.
        * **`precision`**: `[int]` = `None` &rarr; The number of decimal places to display next to the gradient.
        * **`data`**: `[list]` = `None` &rarr; The data for the gradient as a list of dicts.
            * **Note**: See `props_gradient_data` for more information.
        """
        notationDisplay_options_dict = {
            "compact": ["short", "long"],
            "scientific": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "engineering": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "precision": ["e", "e+", "E", "E+", "x10^", "x10^+"],
            "standard": [],
        }
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "scale": ["linear", "log", "pow", "step"],
                "notation": ["standard", "compact", "scientific", "engineering", "precision"],
                "notationDisplay": notationDisplay_options_dict.get(notation, []),
                "notation": ["standard", "compact", "scientific", "engineering", "precision"],
            },
        }

    def __extend_spec__(self, **kwargs):
        props_gradient_scaleParams(
            data=self.data.get("scaleParams", {}),
            log=self.log,
            prepend_path=["scaleParams"],
            gradient_scale_type=self.data.get("scale"),
        )
        if self.data.get("data"):
            for idx, gradient_data in enumerate(self.data.get("data")):
                props_gradient_data(
                    data=gradient_data,
                    log=self.log,
                    prepend_path=["data", idx],
                    **kwargs,
                )


@type_enforced.Enforcer
class props_gradient_scaleParams(ApiValidator):
    @staticmethod
    def spec(
        exponent: float | int | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`exponent`**: `[float | int]` = `None` &rarr; The exponent for the scale if using a power gradient.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        if self.data.get("exponent") is not None:
            if self.data.get("exponent") <= 0:
                self.__error__(msg="`exponent` must be greater than 0 for a power gradient")
        if kwargs.get("gradient_scale_type") == "pow":
            if not self.data.get("exponent"):
                self.__error__(msg="`exponent` must be specified for a power gradient")


@type_enforced.Enforcer
class props_gradient_data(ApiValidator):
    @staticmethod
    def spec(
        value: int | float | str,
        color: str | None = None,
        size: str | None = None,
        label: str | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`value`**: `[int | float | str]` &rarr; The value for the split point in the gradient.
        * **`color`**: `[str]` = `None` &rarr; The color string to use for the split point.
            * **Note**: A valid color string (EG: "RGBA(0,0,0,1)")
        * **`size`**: `[str]` = `None` &rarr; The size string to use for the split point.
            * **Note**: A valid size string (EG: "5px")
        * **`label`**: `[str]` = `None` &rarr; The label to use for the split point.
        """
        accepted_values = {}
        if isinstance(value, str):
            accepted_values = {
                "value": ["min", "max"],
            }
        return {
            "kwargs": kwargs,
            "accepted_values": accepted_values,
        }

    def __extend_spec__(self, **kwargs):
        if self.data.get("color"):
            self.__check_color_string_valid__(color_string=self.data.get("color"))
        if self.data.get("size"):
            self.__check_pixel_string_valid__(pixel_string=self.data.get("size"))


@type_enforced.Enforcer
class props_slider_scaleParams(ApiValidator):
    @staticmethod
    def spec(
        exponent: float | int | None = None,
        base: float | int | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`exponent`**: `[float | int]` = `None` &rarr; The exponent for a power (`"pow"`) scale.
            * **Note**: Required when using a power scale.
        * **`base`**: `[float | int]` = `None` &rarr; The base for a logarithmic (`"log"`) or exponential (`"exp"`) scale.
            * **Notes**:
                * Required when using an exponential scale.
                * If omitted for a logarithmic scale, it defaults to `10`.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        scale = kwargs.get("slider_scale_type") or "linear"
        exponent = self.data.get("exponent")
        base = self.data.get("base")
        if exponent is not None:
            if exponent <= 0:
                self.__error__(msg="`exponent` must be greater than 0 for a power scale")
            if scale != "pow":
                self.__warn__(msg=f"`exponent` has no effect on a `{scale}` scale")
        if base is not None:
            if base <= 0 or base == 1:
                self.__error__(msg="`base` must be greater than 0 and not equal to 1")
            if scale not in ["log", "exp"]:
                self.__warn__(msg=f"`base` has no effect on a `{scale}` scale")
        if scale == "pow" and exponent is None:
            self.__error__(msg="`exponent` must be specified for a power scale")
        if scale == "exp" and base is None:
            self.__error__(msg="`base` must be specified for an exponential scale")


@type_enforced.Enforcer
class layout(ApiValidator):
    @staticmethod
    def spec(
        type: str,
        numColumns: str | int | None = None,
        numRows: str | int | None = None,
        data: dict | None = None,
        itemId: str | None = None,
        column: int | None = None,
        row: int | None = None,
        style: dict | None = None,
        containerStyle: dict | None = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`type`**: `[str]` &rarr; The type of the layout.
            * **Accepted Values**:
                * `"grid"`: A layout element that can contain other layout elements.
                * `"item"`: A layout element where a prop is located.
        * **`numColumns`**: `[str | int]` = `"auto"` &rarr; The number of columns for the grid layout.
            * **Notes**:
                * If `"auto"`, the number of columns will be calculated based on the number of items.
                * This attribute applies exclusively to `"grid"` layouts.
        * **`numRows`**: `[str | int]` = `"auto"` &rarr; The number of rows for the grid layout.
            * **Notes**:
                * If `"auto"`, the number of rows will be calculated based on the number of items.
                * This attribute applies exclusively to `"grid"` layouts.
        * **`data`**: `[dict]` = `None` &rarr; The data for the layout.
            * **Note**: This attribute applies exclusively to `"grid"` layouts.
        * **`itemId`**: `[str]` = `None` &rarr; The id of the prop placed in the layout
            * **Note**: This attribute applies exclusively to `"item"` layouts.
        * **`column`**: `[int]` = `None` &rarr; The column in which to place the prop in the current grid.
        * **`row`**: `[int]` = `None` &rarr; The row in which to place the prop in the current grid.
        * **`style`**: `[dict | None]` = `None` &rarr; Provides an escape hatch for specifying CSS rules.
            * **Note**: In `"item"` layouts, the `style` is applied to the root of the prop container, while in `"grid"` layouts, it targets the CSS Grid layout level.
        * **`containerStyle`**: `[dict | None]` = `None` &rarr; Provides an escape hatch for specifying CSS rules for the container element.
        """
        passed_values = {k: v for k, v in locals().items() if (v is not None) and k != "kwargs"}
        required_fields = ["type"]
        optional_fields = ["style", "containerStyle"]
        if type == "grid":
            required_fields += ["data"]
            optional_fields += ["numColumns", "numRows", "column", "row"]
        elif type == "item":
            required_fields += ["itemId"]
            optional_fields += ["column", "row"]
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
            "accepted_values": accepted_values,
        }

    def __extend_spec__(self, **kwargs):
        layout_type = self.data.get("type", None)
        if layout_type == "grid":
            for field, value in self.data.get("data", {}).items():
                layout(data=value, log=self.log, prepend_path=["data", field], **kwargs)
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
        Accepts all arbitrary values depending on what you have in your props as part of the API spec.

        The values you pass will be validated against the props in your API spec.
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
            if prop_type == "head":
                self.__error__(
                    msg=f"`{prop_key}` with the prop type of `{prop_type}` can not have an associated value."
                )
                continue
            acceptable_types = {
                "num": (int, float),
                "toggle": (bool,),
                "button": (str,),
                "text": (str,),
                "selector": (list,),
                "date": (str,),
                "media": (str,),
                "coordinate": (list,),
            }.get(prop_type, tuple())
            # Add None to acceptable types if allowed
            if prop_spec.get("allowNone", False):
                acceptable_types += (type(None),)
            # Validate types and continue if invalid
            if not self.__check_type__(prop_value, acceptable_types, prepend_path=[prop_key]):
                continue
            # Continue if the value is None
            if prop_value is None:
                continue
            if prop_type == "num":
                min_value = prop_spec.get("minValue", float("-inf"))
                max_value = prop_spec.get("maxValue", float("inf"))
                if prop_value < min_value or prop_value > max_value:
                    self.__error__(
                        msg=f"`{prop_key}` with the prop type of `{prop_type}` must be between {min_value} and {max_value} as defined by the API spec."
                    )
            elif prop_type == "selector":
                options = list(prop_spec.get("options", {}).keys())
                self.__check_subset_valid__(prop_value, options, prepend_path=[prop_key])
            elif prop_type == "date":
                date_variant = prop_spec.get("variant", "date")
                if self.__check_date_valid__(
                    prop_value, date_variant=date_variant, prepend_path=[prop_key]
                ):
                    self.__check_date_constraints__(
                        prop_value, prop_spec, date_variant, prepend_path=[prop_key]
                    )
            elif prop_type == "media":
                if self.__check_url_valid__(prop_value, prepend_path=[prop_key]):
                    self.__check_media_url_variant__(
                        prop_value, variant=prop_spec.get("variant"), prepend_path=[prop_key]
                    )
            elif prop_type == "coordinate":
                coord_variant = prop_spec.get("variant", "latLngMap")
                self.__check_coord_path_valid__(prop_value, coord_variant, prepend_path=[prop_key])


@type_enforced.Enforcer
class valueLists(ApiValidator):
    @staticmethod
    def spec(**kwargs):
        """
        Accepts all arbitrary values depending on what you have in your props as part of the API spec.

        The valueLists you pass will be validated against the `props` from your API spec.
        """
        return {
            "kwargs": {},
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        props_data = kwargs.get("props_data", {})
        for prop_key, prop_value_list in self.data.items():
            if not isinstance(prop_value_list, list):
                self.__error__(
                    msg=f"`{prop_key}` must be a list of values for valueLists", path=[prop_key]
                )
                continue
            prop_spec = props_data.get(prop_key, {})
            if not prop_spec:
                self.__error__(
                    msg=f"`{prop_key}` does not match any valid prop ids {list(props_data.keys())}"
                )
                continue
            prop_type = prop_spec.get("type", None)
            if prop_type == "head":
                self.__error__(
                    msg=f"`{prop_key}` with the prop type of `{prop_type}` can not have an associated value."
                )
                continue
            acceptable_types = {
                "num": (int, float),
                "toggle": (bool,),
                "button": (str,),
                "text": (str,),
                "selector": (list,),
                "date": (str,),
                "media": (str,),
                "coordinate": (list,),
            }.get(prop_type, tuple())
            # Add None to acceptable types if allowed
            if prop_spec.get("allowNone", False):
                acceptable_types += (type(None),)
            if not self.__check_type_list__(
                data=prop_value_list, types=acceptable_types, prepend_path=[prop_key]
            ):
                continue
            if prop_spec.get("allowNone", False):
                prop_value_list = [v for v in prop_value_list if v is not None]
            if prop_type == "num":
                # Validate minimum is met
                min_value = prop_spec.get("minValue")
                if min_value is not None:
                    prop_value_list_min = min(prop_value_list)
                    if prop_value_list_min < min_value:
                        self.__error__(
                            msg=f"`{prop_key}` has a value that is less than {min_value} as defined by the API spec."
                        )
                # Validate maximum is met
                max_value = prop_spec.get("maxValue")
                if max_value is not None:
                    prop_value_list_max = max(prop_value_list)
                    if prop_value_list_max > max_value:
                        self.__error__(
                            msg=f"`{prop_key}` has a value that is greater than {max_value} as defined by the API spec."
                        )
            elif prop_type == "selector":
                options = list(prop_spec.get("options", {}).keys())
                prop_value_list_set = list(set(pamda.flatten(prop_value_list)))
                self.__check_subset_valid__(prop_value_list_set, options, prepend_path=[prop_key])
            elif prop_type == "head":
                self.__error__(
                    msg=f"`{prop_key}` with the prop type of `{prop_type}` can not have an associated value."
                )
            elif prop_type == "date":
                prop_value_list_set = list(set(prop_value_list))
                date_variant = prop_spec.get("variant", "date")
                for prop_value in prop_value_list:
                    if not self.__check_date_valid__(
                        prop_value, date_variant=date_variant, prepend_path=[prop_key]
                    ):
                        continue
                    self.__check_date_constraints__(
                        prop_value, prop_spec, date_variant, prepend_path=[prop_key]
                    )
            elif prop_type == "media":
                for prop_value in prop_value_list:
                    if not self.__check_url_valid__(prop_value, prepend_path=[prop_key]):
                        continue
                    self.__check_media_url_variant__(
                        prop_value, variant=prop_spec.get("variant"), prepend_path=[prop_key]
                    )
            elif prop_type == "coordinate":
                coord_variant = prop_spec.get("variant", "latLngMap")
                for prop_value in prop_value_list:
                    if not self.__check_coord_path_valid__(
                        prop_value, coord_variant, prepend_path=[prop_key]
                    ):
                        continue
