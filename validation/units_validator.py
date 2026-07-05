from .base_validator import BaseValidator, ValidationIssue


class UnitsValidator(BaseValidator):

    """
    Validates engineering units.
    """

    def validate(self, dataset):

        issues = []

        # Future:
        # psi
        # gpm
        # ft
        # m
        # rpm
        # etc.

        return issues