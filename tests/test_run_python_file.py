from functions.run_python_file import run_python_file


def run_test(name, result):
    print(f"{name}:\n{result}\n")


run_test(
    "test1",
    run_python_file("calculator", "main.py"),
)

run_test(
    "test2",
    run_python_file("calculator", "main.py", ["3 + 5"]),
)

run_test(
    "test3",
    run_python_file("calculator", "tests.py"),
)

run_test(
    "test4",
    run_python_file("calculator", "../main.py"),
)

run_test(
    "test5",
    run_python_file("calculator", "nonexistent.py"),
)

run_test(
    "test6",
    run_python_file("calculator", "lorem.txt"),
)
