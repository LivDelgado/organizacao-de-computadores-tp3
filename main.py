import sys

from computer.cpu import CPU

FILE_NAME = "result.txt"


def initialize_cpu(file_path: str) -> None:
    """
    method responsible for creating the CPU and calling its process method
    :param file_path: path to the file with the instructions to be executed
    :return: None - the output is a txt file (result.txt)
    """
    cpu = CPU(file_path)
    result = cpu.process()
    write_result_to_file(result)


def write_result_to_file(result: str) -> None:
    """
    method responsible to write the result from instructions execution on a file
    :param result: CPU process output
    :return: None
    """
    file = open(FILE_NAME, "w")
    file.write(result)
    file.close()


if __name__ == '__main__':
    initialize_cpu(sys.argv[1])
