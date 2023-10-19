## API Reference

This code serves as a generic API spec. It is used to automate the API documentation process.

Submodules are used to define the api spec for each level of the api. You can use the links on the left to navigate into the API and get detailed documentation for each API item at each level.

Classes represent the actual API items and should have relevant API documentation for each item at the class level.

For example, you are currently in the root of the API spec. In the API root, you can find the following submodules like `kwargs` and `settings`. See the left hand side for all available submodules.


## Validation Use

This code can be used directly for validation purposes:

```
from cave_utils.api_spec import Validator

session_data = {
    "kwargs": {
        "wipeExisting": True,
    },
    # All of your session data to validate here
}

x=Validator(
    session_data=session_data,
)

print(x.log.log)
```