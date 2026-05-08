# Error Handling Rules

Pick ONE project strategy:

- exceptions
- expected<T, Error>
- Result<T>
- error_code

Do not mix styles randomly.

## General Rules

- Errors must propagate clearly.
- Log at boundaries.
- Avoid silent failure.
