import sys

from computer.cpu import CPU

FILE_NAME = "result.txt"


def initialize_cpu(file_path: str) -> None:
    cpu = CPU(file_path)
    result = cpu.process()
    write_result_to_file(result)


def write_result_to_file(result: str) -> None:
    file = open(FILE_NAME, "w")
    file.write(result)
    file.close()


if __name__ == '__main__':
    initialize_cpu(sys.argv[1])
