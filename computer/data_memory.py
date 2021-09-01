from typing import Dict, Optional


class DataMemory:  # TODO
    def __init__(self):
        self.memory: Dict[str, str]

    def read(self) -> Optional[str]:
        """
        read from data memory
        :return: data in the address, if found
        """
        print("hehehe")

    def write(self) -> None:
        """
        write to data memory
        :return: None
        """
        print("hihihi")
