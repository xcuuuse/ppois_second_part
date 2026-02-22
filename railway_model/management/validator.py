from exceptions.exceptions import CreatingEntityError
from typing import Dict


class Validator:
    @classmethod
    def validate(cls, data: dict, rules: Dict[str, tuple]):
        for field, (expected_type, validator_func) in rules.items():
            value = data.get(field)
            if not isinstance(value, expected_type):
                raise CreatingEntityError(f"Field '{field}' is not of type {expected_type.__name__}")
            if validator_func and not validator_func(value):
                raise CreatingEntityError(f"Field '{field}' does not satisfy validation rule")