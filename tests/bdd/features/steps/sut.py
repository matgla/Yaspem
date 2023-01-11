import pathlib
import os
import platform
import subprocess
import shutil
import stat

from behave import *

working_dir = pathlib.Path(__file__).parent.parent.parent.parent.parent
test_dir = pathlib.Path(__file__).parent.parent
python_executable = "Scripts/python.exe" if platform.system() == "Windows" else "bin/python3"

def expectation_msg(context, expectation):
    return "\n------------------------------\nExpected: " + expectation + "\n" + "Stdout: " \
        + context.stdout + "\n" + "Stderr: " + context.stderr + "---------------------------\n"

def file_expectation_msg(expectation, content):
    return "\n------------------------------\nExpected file content: " + expectation + "\n" + "Readed: " \
        + content + "\n---------------------------\n"

def execute_sut(context, args = []):
    root_dir = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
    python_path = root_dir / "test_env" / python_executable
    yaspem_path = root_dir / "yaspem.py"
    args_to_run = [str(python_path), str(yaspem_path)]
    args_to_run.extend(args)
    rc = subprocess.run(args_to_run, cwd=working_dir.absolute(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if context.output_dir:
        with open(context.output_dir / "yaspem.log", "w") as f:
            f.write(rc.stdout)
    return rc

@given('we have YASPEM executable')
def step_impl(context):
    context.executable = execute_sut
    context.output_dir = None

@when('we execute with dependency file')
def step_impl(context):
    if context.output_dir:
        context.executable(context, ["-o " + context.output_dir])
    else:
        context.executable(context)


@when('we execute with arguments')
def step_impl(context):
    args = []
    for row in context.table:
        args.append(row["argument"]
            .replace("${data_dir}", str(test_dir / "data"))
            .replace("${test_output_dir}", "test_output")
        )

    if context.output_dir:
        args.append("-o " + str(context.output_dir))

    context.output = context.executable(context, args)
    context.stdout = context.output.stdout

def rmdirReadOnly(action, name, exec):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

@Given('output directory')
def step_impl(context):
    context.output_dir = working_dir / pathlib.Path("test_output") / pathlib.Path(context.text) 
    if os.path.exists(context.output_dir):
        shutil.rmtree(context.output_dir, onerror=rmdirReadOnly)

@then('YASPEM will show usage text')
def step_impl(context):
    assert "usage:" in context.stdout

@then('YASPEM will show required argument')
def step_impl(context):
    arguments = ""
    for row in context.table:
        arguments = arguments + row["argument"]

    print(arguments)
    expected_error = "error: the following arguments are required: " + arguments
    assert expected_error in context.stdout, expectation_msg(context, expected_error)

@then('YASPEM will show error')
def step_impl(context):
    expected_error = context.table[0]['text']
    assert expected_error in context.stdout, expectation_msg(context, expected_error)

@then('YASPEM will return error code')
def step_impl(context):
    assert context.output.returncode != 0

@then('YASPEM will return 0')
def step_impl(context):
    assert context.output.returncode == 0

@then('YASPEM will fetch it')
def step_impl(context):
    pass

@then('Fetched package contains files')
def step_impl(context):
    for row in context.table:
        package_dir = context.output_dir / "packages" / "sources" / row["package"]
        assert os.path.exists(package_dir), "Expected path: " + str(package_dir)
        file_dir = package_dir / row["file"]
        assert os.path.exists(file_dir)
        with open(file_dir, "r") as file:
            file_content = file.read()
            assert row["content"] in file_content, file_expectation_msg(row["content"], file_content)

@then('CMake Modules are empty')
def step_impl(context):
    modules_dir = context.output_dir / "packages" / "modules"
    assert os.path.exists(modules_dir), "Path not exists: " + str(modules_dir)
    assert len(os.listdir(modules_dir)) == 0

@then('Fetched module contains files')
def step_impl(context):
    for row in context.table:
        module_dir = context.output_dir / "packages" / "modules"
        assert os.path.exists(module_dir), "Expected path: " + str(module_dir)
        file_dir = module_dir / row["file"]
        assert os.path.exists(file_dir)

@then('CMake is able to find new module')
def step_impl(context):
    pass
