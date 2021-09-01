from computer.cache import Cache
from computer.data_memory import DataMemory
from computer.decoder import Decoder
from computer.instruction_memory import InstructionMemory


class CPU:
    def __init__(self, file_path):
        self.file_path = file_path
        self.decoder: Decoder = Decoder(file_path)
        self.instruction_memory: InstructionMemory = InstructionMemory()
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

    # MAIN METHOD - will be called by main.py file
    # returns string that will be written in the output file
    def process(self) -> str:
        self.decode()
        return self.get_instructions_outputs()

    def decode(self) -> None:
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

    def get_instructions_outputs(self) -> str:
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
