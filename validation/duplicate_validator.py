from .base_validator import BaseValidator, ValidationIssue


class DuplicateValidator(BaseValidator):

    def validate(self, dataset):

        issues = []

        df = dataset.raw_dataframe

        if df is None:
            return issues

        duplicates = df.duplicated().sum()

        if duplicates > 0:

            issues.append(

                ValidationIssue(

                    category="Duplicates",

                    severity="WARNING",

                    message=f"{duplicates} duplicate rows found.",

                    recommendation="Review duplicate records."

                )

            )

        return issues