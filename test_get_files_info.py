from functions.get_files_info import get_files_info

def run_case(title: str, working_dir: str, path: str, indent_error: bool = False):
    print(f"Result for {title}:")

    result = get_files_info(working_dir, path)

    if result.startswith("Error:"):
        if indent_error:
            print("    " + result)
        else:
            print(result)
    else:
        print(result)

    print()


def main():
    run_case("current directory", "calculator", ".")
    run_case("'pkg' directory", "calculator", "pkg")
    run_case("'/bin' directory", "calculator", "/bin", indent_error=True)
    run_case("'../' directory", "calculator", "../", indent_error=True)


if __name__ == "__main__":
    main()
