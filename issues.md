
# Static Code Analysis Issues

The original `parcel_tracker.py` file was checked using Pylint, Bandit, and Flake8 before making any changes.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `subprocess.check_output()` with `shell=True` | Security – High | 55 | Running a command through the shell with a dynamically constructed string can create command-injection risks. | Pass command arguments as a list and avoid `shell=True`. |
| Use of `tempfile.mktemp()` | Security – Medium | 50 | The function generates a temporary filename without safely creating the file, which can cause a race condition. | Use a safer function such as `tempfile.NamedTemporaryFile()`. |
| Mutable default argument `[]` | Code Quality | 11 | A mutable default list can be shared between function calls and cause unexpected behaviour. | Use `None` as the default and create a new list inside the function. |
| Use of `random.randint()` for delivery OTP | Security | 72 | The standard pseudo-random generator is unsuitable for security-sensitive OTP generation. | Use `secrets.randbelow()` or another cryptographically secure generator. |
| Missing module and function docstrings | Code Quality | 1, 11, 20, 27, 34, 43, 48, 53 | The module and several functions lack descriptions, making the code harder to understand. | Add clear docstrings describing the purpose of the module and each function. |
| Names do not follow `snake_case` | Code Style | 11, 20, 27, 34, 43, 48, 53 | Function names and some arguments use camelCase rather than the conventional Python naming style. | Rename functions and arguments using `snake_case` and update their calls. |
| Missing whitespace around an operator | Code Style | 28 | An operator does not have the required surrounding whitespace. | Add spaces around the operator. |
| Missing space after a comma | Code Style | 74 | A comma is not followed by a space, reducing readability. | Add a space after the comma. |
