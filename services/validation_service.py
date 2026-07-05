from validation.file_validator import FileValidator
from validation.missing_validator import MissingValidator
from validation.duplicate_validator import DuplicateValidator
from validation.timestamp_validator import TimestampValidator
from validation.units_validator import UnitsValidator
from validation.survey_validator import SurveyValidator
from validation.engineering_validator import EngineeringValidator
from validation.quality_score import QualityScore


class ValidationService:
    """
    Enterprise Validation Service

    Coordinates all validators and returns
    a single validation report.
    """

    def __init__(self):

        self.validators = [

            FileValidator(),

            MissingValidator(),

            DuplicateValidator(),

            TimestampValidator(),

            UnitsValidator(),

            SurveyValidator(),

            EngineeringValidator()

        ]

    def validate(self, dataset):

        all_issues = []

        for validator in self.validators:

            try:

                issues = validator.validate(dataset)

                if issues:
                    all_issues.extend(issues)

            except Exception as ex:

                all_issues.append(
                    {
                        "validator": validator.__class__.__name__,
                        "severity": "ERROR",
                        "message": str(ex)
                    }
                )

        score = QualityScore.calculate(all_issues)

        return {

            "status": "PASS" if score >= 90 else "REVIEW",

            "quality_score": score,

            "issues": all_issues,

            "total_issues": len(all_issues)

        }