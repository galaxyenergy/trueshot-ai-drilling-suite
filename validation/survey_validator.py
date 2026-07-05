from .base_validator import BaseValidator, ValidationIssue


class SurveyValidator(BaseValidator):

    """
    Survey integrity validator.
    Never modifies survey stations.
    """

    def validate(self, dataset):

        issues = []

        # Future:
        # MD increasing
        # Inc limits
        # Azi limits
        # Duplicate stations
        # Missing stations

        return issues