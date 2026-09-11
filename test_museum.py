from gui import detect_error_type, categorize_error


def test_name_error():

    result = detect_error_type(
        "NameError: name 'x' is not defined"
    )

    assert result == "NameError"


def test_syntax_error():

    result = detect_error_type(
        "SyntaxError: invalid syntax"
    )

    assert result == "SyntaxError"


def test_type_error():

    result = detect_error_type(
        "TypeError: unsupported operand type"
    )

    assert result == "TypeError"


def test_indentation_error():

    result = detect_error_type(
        "IndentationError: unexpected indent"
    )

    assert result == "IndentationError"


def test_unknown_error():

    result = detect_error_type(
        "Something completely unknown happened"
    )

    assert result == "Unknown Error"


def test_category():

    result = categorize_error("NameError")

    assert result == "Variable / Naming Problem"