from typing import Dict, Optional


class Cache:  # TODO
    def __init__(self):
        self.memory: Dict[str, Block]

    def read(self) -> Optional[str]:
        """
        read from cache memory
        :return: data in the address, if found
        """
        print("hehehe")

    def write(self) -> None:
        """
        write to cache memory
        :return: None
        """
        print("hihihi")
        # tag block as dirty


class Block:
    def __init__(self):
        self.tag: str
        self.data: str
        self.dirty: bool
