class QualityScore:

    @staticmethod
    def calculate(issues):

        if not issues:
            return 100.0

        deductions = 0

        for issue in issues:

            severity = ""

            if isinstance(issue, dict):
                severity = issue.get("severity", "").upper()

            else:
                severity = getattr(issue, "severity", "").upper()

            if severity == "CRITICAL":
                deductions += 20

            elif severity == "ERROR":
                deductions += 10

            elif severity == "WARNING":
                deductions += 5

            else:
                deductions += 1

        score = max(0, 100 - deductions)

        return float(score)
    