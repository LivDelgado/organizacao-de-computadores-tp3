from typing import Tuple

from computer.cache import Cache
from computer.decoder import Decoder
from computer.instruction_memory import *


class CPU:
    def __init__(self, file_path):
        self.instruction_memory: InstructionMemory = InstructionMemory()
        self.decoder: Decoder = Decoder(file_path, self.instruction_memory)
        self.l1_memory: Cache = Cache()

        self.hit_count: int = 0
        self.miss_count: int = 0

    @property
    def hit_rate(self):
        return round(self.hit_count/self.instruction_memory.count_read_instructions(), 3)

    @property
    def miss_rate(self):
        return round(self.miss_count/self.instruction_memory.count_read_instructions(), 3)

    def increment_miss_count(self) -> None:
        """
        increment miss count by one
        :return: None
        """
        self.miss_count += 1

    def increment_hit_count(self):
        """
        increment hit count by one
        :return: None
        """
        self.hit_count += 1

    def process(self) -> str:
        """
        cpu main method
        :return: string with output from cpu execution
        """
        self.decoder.decode()
        self.execute_instructions()
        return self.get_instructions_outputs()

    def execute_instructions(self) -> None:
        """
        execute all instructions in the instruction memory
        :return: None
        """
        for instruction in self.instruction_memory.instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction) -> None:
        """
        executes a single Instruction
        :param instruction: instruction to be executed
        :return: None
        """
        if instruction.operation_type == OperationType.READ:  # read instruction
            result, data = self.read_from_memory(instruction)
            instruction.change_result(result)
        else:  # write instruction
            instruction.change_result(InstructionResult.WROTE)
            self.write_data(instruction)

    def read_from_memory(self, instruction) -> Tuple[InstructionResult, List[str]]:
        """
        read data from memory - controls the whole reading op
        :param instruction: read instruction to be executed
        :return: instruction result and data read
        """
        hit, data = self.l1_memory.read(address=instruction.address)
        if hit:
            self.increment_hit_count()
            return InstructionResult.HIT, data
        else:
            self.increment_miss_count()
            return InstructionResult.MISS, data

    def write_data(self, instruction) -> None:
        """
        if block in cache is already dirty, update data memory with current cache value and then update cache
        else, add value in cache memory and tag it as dirty
        :param instruction: write instruction to be executed
        :return: None
        """
        self.l1_memory.write(instruction.address, instruction.write_data)

    def get_instructions_outputs(self) -> str:
        """
        return instructions execution as a string
        :return: string with instructions output information
        """
        outputs = (
            f"READS: {self.instruction_memory.count_read_instructions()}\n"
            f"WRITES: {self.instruction_memory.count_write_instructions()}\n"
            f"HITS: {self.hit_count}\n"
            f"MISSES: {self.miss_count}\n"
            f"HIT RATE: {self.hit_rate}\n"
            f"MISS RATE: {self.miss_rate}\n"
        )

        outputs += "\n"

        for instruction in self.instruction_memory.instructions:
            outputs += str(instruction) + "\n"

        return outputs
