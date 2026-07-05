from .base_validator import BaseValidator, ValidationIssue


class FileValidator(BaseValidator):

    def validate(self, dataset):

        issues = []

        if dataset is None:

            issues.append(
                ValidationIssue(
                    category="File",
                    severity="CRITICAL",
                    message="No dataset supplied.",
                    recommendation="Import a WellData Shift Export."
                )
            )

            return issues

        if dataset.raw_dataframe is None:

            issues.append(
                ValidationIssue(
                    category="File",
                    severity="CRITICAL",
                    message="Dataset has no dataframe.",
                    recommendation="Reload the shift export."
                )
            )

            return issues

        if dataset.raw_dataframe.empty:

            issues.append(
                ValidationIssue(
                    category="File",
                    severity="CRITICAL",
                    message="Dataset is empty.",
                    recommendation="Verify the exported file."
                )
            )

        return issues