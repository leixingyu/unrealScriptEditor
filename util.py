import unreal


def execute_python_command(command):
    return unreal.PythonScriptLibrary.execute_python_command_ex(
        python_command=command,
        execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
        file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
    )

