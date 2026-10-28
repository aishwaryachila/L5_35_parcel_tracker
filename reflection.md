
# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis?

Static code analysis checks source code without executing the program. Tools such as Pylint, Bandit, and Flake8 help identify coding mistakes, security risks, and style problems.

### 2. What issues did you find in your program?

I found naming convention problems, missing docstrings, an unsafe mutable default argument, a broad exception handler, and security issues involving temporary files, subprocess commands, and random number generation.

### 3. How did you fix the issues?

I improved function and variable names, added docstrings, replaced the mutable default argument with a safer approach, handled specific exceptions, and improved the security of temporary file creation, subprocess execution, and OTP generation. I also corrected formatting issues.

### 4. Why is static code analysis important?

Static code analysis helps improve code quality, readability, maintainability, and security. It can detect potential problems early, before they cause failures or vulnerabilities when the program runs.
