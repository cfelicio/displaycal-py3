import sys

import pytest


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_execaction_filters_none_values_in_args_and_will_not_raise_errors():
    """ExecAction will filter any None values in the args list and will not raise any errors."""
    from DisplayCAL.taskscheduler import ExecAction

    ea = ExecAction(cmd="", args=[None])  # This should not raise any errors.
    ea_no_args = ExecAction(cmd="")  # Default args=None should not raise TypeError.
    assert ea["arguments"] is None
    assert ea_no_args["arguments"] is None


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_task_str_returns_str():
    """Task.__str__() should return a str in Python 3, not bytes."""
    from DisplayCAL.taskscheduler import Task

    task = Task(name="TestTask", author="TestAuthor")
    result = str(task)
    assert isinstance(result, str)
    assert '<?xml version="1.0" encoding="UTF-16"?>' in result
    assert "<Task" in result
    assert "<Author>TestAuthor</Author>" in result


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_task_write_xml(tmp_path):
    """Task.write_xml() should write valid UTF-16 XML with BOM."""
    import codecs
    from DisplayCAL.taskscheduler import Task

    task = Task(name="TestTask", author="TestAuthor")
    xml_file = str(tmp_path / "task.xml")
    task.write_xml(xml_file)

    with open(xml_file, "rb") as f:
        content = f.read()

    assert content.startswith(codecs.BOM_UTF16_LE)
    decoded = content.decode("UTF-16")
    assert "<Author>TestAuthor</Author>" in decoded

