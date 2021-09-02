from typing import Dict, Optional, List


class DataMemory:
    def __init__(self):
        self.memory: Dict[str, List[str]] = {}
        self.size_byte_offset = 4

    def read(self, address: str) -> List[str]:
        """
        read from data memory
        :return: data in the address, if found
        """
        return self.memory.get(address[:-self.size_byte_offset])

    def write(self, address: str, data: List[str]) -> None:
        """
        write to data memory
        :return: None
        """
        self.memory[address[:-self.size_byte_offset]] = data
