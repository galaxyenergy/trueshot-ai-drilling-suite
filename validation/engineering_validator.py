from .base_validator import BaseValidator, ValidationIssue


class EngineeringValidator(BaseValidator):

    """
    Engineering sanity checks.
    """

    def validate(self, dataset):

        issues = []

        # Future:
        # WOB
        # RPM
        # Flow
        # SPP
        # Torque
        # ROP

        return issues