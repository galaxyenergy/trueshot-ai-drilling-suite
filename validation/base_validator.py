from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ValidationIssue:
    """
    Standard validation issue used throughout the platform.
    """

    category: str
    severity: str
    message: str
    recommendation: str = ""
    auto_fix: bool = False


class BaseValidator(ABC):
    """
    Base class for every validator.
    """

    @abstractmethod
    def validate(self, dataset):
        """
        Returns a list of ValidationIssue objects.
        """
        pass