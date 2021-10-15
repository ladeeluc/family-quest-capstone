# Installation & Usage
You must have the Python package manager [poetry](https://https://python-poetry.org/) to run this application.

After cloning the repo, create a `.env` file and fill it in using this template as reference:

```
DEBUG=True|False
SECRET_KEY="somesecretkeyhere"
```
Then run these commands to start the app:

1. `poetry install`
1. `poetry shell`
1. `python manage.py runserver`
1. `python -m webbrowser "localhost:8000"`

# Quality/Style Standards
**General**
- Use trailing commas for multiline lists, tuples, dicts, and function args
- Use single quotes `''` over double quotes `""` unless double quotes are necessary, such as:
  - Strings nested in f-strings:
    ```python
    f"Hello {something('World!')}"
    ```
  - Single quote needed in the string:
    ```python
    "That's it!"
    ```

**Views**
- All views are class based
- Base views have a docstring describing how to use/extend the class

**Models**
- All models have a `__str__` method
- All models are registered in the admin panel

**Forms**
- All forms use the same field names as the model they relate to

