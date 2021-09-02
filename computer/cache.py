from typing import Dict, Optional


class Cache:  # TODO
    def __init__(self):
        # str -> index, Block -> memory block
        self.memory: Dict[str, Block]

    def read(self, address: str) -> Optional[str]:
        """
        read from cache memory
        :return: data in the address, if found
        """

        # convert address to binary
        binary_address = str(bin(int(address))).rjust(32, '0')
        print(binary_address)
        return ""

    def write(self) -> None:
        """
        write to cache memory
        :return: None
        """
        print("hihihi")
        # tag block as dirty


class Block:
    def __init__(self):
        self.offset: str  # offset of 4 bits
        self.tag: str  # tag to identify data on address
        self.data: str  # data saved in the address
        self.dirty: bool  # if the block was already written
