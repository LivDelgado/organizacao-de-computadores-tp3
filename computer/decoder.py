from computer.instruction_memory import InstructionMemory


class Decoder:
    def __init__(self, file_path: str, instruction_memory: InstructionMemory):
        self.file_path: str = file_path
        self.instruction_memory = instruction_memory

    def decode(self) -> None:
        """
        decodes file lines to instructions
        :return: None
        """
        file = open(self.file_path, "r")
        file_lines = str.splitlines(file.read())
        file.close()

        for line in file_lines:
            instruction_information = line.split(' ')
            self.instruction_memory.add_instruction(
                address=instruction_information[0],
                operation_type=int(instruction_information[1]),
                write_data=instruction_information[2] if (len(instruction_information) > 2) else None
            )

