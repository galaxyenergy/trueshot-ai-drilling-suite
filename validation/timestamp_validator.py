from .base_validator import BaseValidator, ValidationIssue


class TimestampValidator(BaseValidator):

    """
    Validates timestamp integrity.
    """

    def validate(self, dataset):

        issues = []

        df = dataset.raw_dataframe

        if df is None:
            return issues

        # Future implementation:
        # Verify chronological order
        # Detect duplicate timestamps
        # Detect missing time intervals

        return issues