from dataclasses import dataclass

from lint_rules._core.source.source_location import SourceLocation
from lint_rules._core.violation import Violation


@dataclass(frozen=True)
class FakeViolation(Violation):
    @property
    def message(self) -> str:
        return "message"


def test_str_without_location():
    assert str(FakeViolation("a.py")) == "a.py: message"


def test_str_with_location():
    assert str(FakeViolation("a.py", SourceLocation(3, 5))) == "a.py:3:5: message"
