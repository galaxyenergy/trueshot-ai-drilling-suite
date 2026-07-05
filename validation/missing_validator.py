from .base_validator import BaseValidator, ValidationIssue


class MissingValidator(BaseValidator):

    def validate(self, dataset):

        issues = []

        df = dataset.raw_dataframe

        if df is None:
            return issues

        missing = df.isnull().sum()

        for column, count in missing.items():

            if count > 0:

                issues.append(

                    ValidationIssue(

                        category="Missing Data",

                        severity="WARNING",

                        message=f"{column} has {count} missing values.",

                        recommendation="Review imported WellData export."

                    )

                )

        return issues