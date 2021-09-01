from enum import Enum
from typing import Optional, List


class InstructionMemory:
    def __init__(self):
        self.instructions: List[Instruction] = []

    def add_instruction(self, address: str, operation_type: int, write_data: Optional[str]) -> None:
        self.instructions.append(Instruction(address, operation_type, write_data))

    def count_read_instructions(self) -> int:
        return len([i for i in self.instructions if i.operation_type is OperationType.READ])

    def count_write_instructions(self) -> int:
        return len([i for i in self.instructions if i.operation_type is OperationType.WRITE])


class Instruction:
    def __init__(self, address: str, operation_type: int, write_data: Optional[str]):
        self.address: str = address  # memory address
        self.operation_type: OperationType = OperationType(operation_type)  # read or write (enum)
        self.write_data: str = write_data  # if it is going to write, it should have a write data
        self.result: Optional[InstructionResult] = InstructionResult.DEFAULT  # result of the instruction execution

    def __str__(self):
        string_self = f"{self.address} {int(self.operation_type.value)}"

        if self.write_data:
            string_self += f" {self.write_data}"

        string_self += f" {self.result.value}"

        return string_self

    def change_result(self, result):
        self.result = result


class OperationType(Enum):
    READ = 0
    WRITE = 1


class InstructionResult(Enum):
    DEFAULT = ""
    WROTE = "W"
    HIT = "H"
    MISS = "M"
