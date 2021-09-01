from typing import Tuple

from computer.cache import Cache
from computer.data_memory import DataMemory
from computer.decoder import Decoder
from computer.instruction_memory import *


class CPU:
    def __init__(self, file_path):
        self.instruction_memory: InstructionMemory = InstructionMemory()
        self.decoder: Decoder = Decoder(file_path, self.instruction_memory)
        self.l1_memory: Cache = Cache()
        self.l2_memory: DataMemory = DataMemory()

        self.hit_count: int = 0
        self.miss_count: int = 0

    @property
    def hit_rate(self):
        return self.hit_count/self.instruction_memory.count_read_instructions()

    @property
    def miss_rate(self):
        return self.miss_count/self.instruction_memory.count_read_instructions()

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

    def read_from_memory(self, instruction) -> Tuple[InstructionResult, str]:
        """
        read data from memory - controls the whole reading op
        :param instruction: read instruction to be executed
        :return: instruction result and data read
        """
        data = self.read_from_l1(instruction.address)
        if data:
            return InstructionResult.HIT, data

        # didn't find data in cache memory, will look for it on data memory
        data = self.read_from_l2(instruction.address)
        # TODO: save data to l1
        return InstructionResult.MISS, data

    def read_from_l1(self, address: str) -> Optional[str]:
        """
        read data from L1 memory (in this case, cache)
        :param address: address to be read from
        :return: data read in the address, if found
        """
        return None # TODO

    def read_from_l2(self, address: str) -> Optional[str]:
        """
        read data from L2 memory (in this case, memory data)
        :param address: address to be read from
        :return: data read in the address, if found
        """
        return None # TODO

    def write_data(self, instruction) -> None:
        """
        if block in cache is already dirty, update data memory with current cache value and then update cache
        else, add value in cache memory and tag it as dirty
        :param instruction: write instruction to be executed
        :return: None
        """
        # TODO

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
