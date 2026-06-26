import os


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


