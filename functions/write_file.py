import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory, creating parent directories if needed and overwriting any existing file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # security boundary check
        if os.path.commonpath([working_dir_abs, target_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # reject directories
        if os.path.isdir(target_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # ensure parent directories exist
        parent_dir = os.path.dirname(target_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # write file
        with open(target_abs, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
