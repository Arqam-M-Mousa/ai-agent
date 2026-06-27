from functions.write_file import write_file


def run_test(name, result):
    print(f"{name}: {result}")


run_test(
    "test1",
    write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
)

run_test(
    "test2",
    write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
)

run_test(
    "test3",
    write_file("calculator", "/tmp/temp.txt", "this should not be allowed"),
)
