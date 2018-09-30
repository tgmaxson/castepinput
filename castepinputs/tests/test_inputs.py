"""
Test module for the inputs
"""
import os
from castepinputs.inputs import CastepInput
from castepinputs.inputs import Block
import pytest


@pytest.fixture
def basic_input():
    c = CastepInput()
    c["a"] = "a"
    c["b"] = Block(["a", "b"])
    c["c"] = 5
    return c


def test_input_gen(basic_input):
    """
    Test basic function of generate inputs
    """
    lines = basic_input.get_file_lines()
    assert lines[0].split(":")[0].strip() == "a"
    assert lines[0].split(":")[1].strip() == "a"
    assert lines[1].startswith("%")
    assert lines[4].startswith("%")


def test_header(basic_input):
    """
    Test adding header
    """
    basic_input.header = ["Hello World"]
    lines = basic_input.get_file_lines()
    assert lines[0] == "# Hello World"

    basic_input.header = ["#Hello World"]
    lines = basic_input.get_file_lines()
    assert lines[0] == "#Hello World"


def test_unit(basic_input):
    """
    Test the unit system
    """
    basic_input.units["a"] = "eV"
    basic_input.units["b"] = "eV"
    lines = basic_input.get_file_lines()
    assert lines[0].split(":")[1].strip()[-2:] == "eV"
    assert lines[2].strip() == "eV"


def test_string(basic_input):
    lines = basic_input.get_file_lines()
    "\n".join(lines) == basic_input.get_string()


def test_save(basic_input, tmpdir):
    outname = str(tmpdir.join("test.in"))
    basic_input.save(outname)
    os.remove(outname)


def test_read_save(basic_input, tmpdir):
    outname = str(tmpdir.join("test.in"))
    basic_input.save(outname)
    input2 = CastepInput()
    input2.load_file(outname)
    assert dict(input2) == dict(basic_input)
