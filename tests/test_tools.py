from collections import OrderedDict

from cloudformation_utils import (
    cloudformation_yaml_loads,
    process_script,
    process_script_decorated,
)

SHELL_RES = [
    "#!/bin/bash -xe\n",
    "\n",
    "CF_Foo='",
    OrderedDict([("Ref", "Foo")]),
    "'\n",
    "Foo='",
    OrderedDict([("Ref", "MyParam")]),
    "'\n",
]
JAVASCRIPT_RES = [
    "var CF_foo='",
    OrderedDict(
        [
            ("Ref", "foo"),
            ("__source", "tests/javascript.js"),
            ("__source_line", "1"),
            ("__optional", "true"),
            ("__default", "default"),
        ]
    ),
    "';\n",
]
PS_RES = [
    "$FOO = '",
    OrderedDict([("Ref", "Bar")]),
    "'\r\n",
    "echo $FOO\n",
    "$FOO = '",
    OrderedDict([("Ref", "Bar")]),
    "'\r\n",
]
PS_RES_DECORATED = [
    "$FOO = '",
    OrderedDict(
        [("Ref", "Bar"), ("__source", "tests/powershell.ps1"), ("__source_line", "1")]
    ),
    "'\r\n",
    "echo $FOO\n",
    "$FOO = '",
    OrderedDict(
        [
            ("Ref", "Bar"),
            ("__source", "tests/powershell.ps1"),
            ("__source_line", "3"),
            ("__optional", "true"),
            ("__default", ""),
        ]
    ),
    "'\r\n",
]


def test_shellscript():
    assert process_script("tests/shell.sh") == SHELL_RES


def test_js():
    assert process_script_decorated("tests/javascript.js") == JAVASCRIPT_RES


def test_ps1():
    assert process_script("tests/powershell.ps1") == PS_RES


def test_ps1_decorated():
    assert process_script_decorated("tests/powershell.ps1") == PS_RES_DECORATED


def test_yaml_loads():
    assert (
        cloudformation_yaml_loads("---\ntest: foo\ntest2: [ bar, baz ]")["test2"][0]
        == "bar"
    )


def test_inline_replacement():
    """Test that hits line 279 - IN_PLACE_RE regex matching with prefix text"""
    result = process_script("tests/inline_test.txt")

    # Expected result for "prefix text $CF{MyParam} suffix text"
    expected = [
        "prefix text ",  # This is result.group(1) that gets appended on line 279
        OrderedDict([("Ref", "MyParam")]),
        " suffix text",
        "another line with ",  # This is another result.group(1)
        OrderedDict([("Ref", "AnotherParam")]),
        " and more text",
    ]

    assert result == expected
