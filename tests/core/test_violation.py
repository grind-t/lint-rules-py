from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violation import Violation


def test_str_without_location():
    assert str(Violation("a.py", "message")) == "a.py: message"


def test_str_with_location():
    assert (
        str(Violation("a.py", "message", SourceLocation(3, 5))) == "a.py:3:5: message"
    )
