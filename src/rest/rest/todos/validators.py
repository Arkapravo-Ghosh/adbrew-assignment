from typing import Any

from ..exceptions import InvalidInputError

MAX_DESCRIPTION_LENGTH = 500


def validate_create_payload(payload: Any) -> str:
    """Return the cleaned description from a create-todo request body."""
    if not isinstance(payload, dict):
        raise InvalidInputError("Request body must be a JSON object.")

    description = payload.get("description")
    if not isinstance(description, str):
        raise InvalidInputError("'description' is required and must be a string.")

    description = description.strip()
    if not description:
        raise InvalidInputError("'description' must not be blank.")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise InvalidInputError(
            f"'description' must be at most {MAX_DESCRIPTION_LENGTH} characters."
        )

    return description
