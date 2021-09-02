from typing import Dict, List, Tuple

from computer.data_memory import DataMemory
from utils.converter import convert_to_32_bit, convert_to_2_bit


class Cache:
    def __init__(self):
        self.l2_memory: DataMemory = DataMemory()
        self.number_of_words_in_block: int = 4
        self.size_byte_offset: int = 2
        self.size_word_offset: int = 2
        self.size_index: int = 6

        # str -> index, Block -> memory block
        self.memory: Dict[str, Block] = {}

    @property
    def total_offset(self):
        return self.size_byte_offset + self.size_word_offset

    def read(self, address: str) -> Tuple[bool, List[str]]:
        """
        read from cache memory
        :return: if it was a hit and data in the address, if found
        """
        block = self.get_cache_block(address)

        binary_address = convert_to_32_bit(address)
        tag = binary_address[:-(self.total_offset + self.size_index)]
        offset = binary_address[-self.total_offset:]

        if block and block.tag == tag and block.valid:  # this will test for a hit
            return True, block.data

        index = self.get_index(address)
        if block and block.dirty:
            self.load_data_from_cache_to_l2_memory(address, block, index)
        if not block:
            self.memory[index] = Block()
            block = self.get_cache_block(address)

        self.update_fresh_data_block(block, tag, offset)
        self.load_data_from_l2_memory(address, block)

        return False, []

    def write(self, address: str, data: str) -> None:
        """
        write to cache memory
        :return: None
        """
        block = self.get_cache_block(address)
        index = self.get_index(address)

        if not block:
            self.memory[index] = Block()
            block = self.get_cache_block(address)

        binary_address = convert_to_32_bit(address)
        tag = binary_address[:-(self.total_offset + self.size_index)]
        offset = binary_address[-self.total_offset:]

        word_index = binary_address[-self.total_offset:-self.size_byte_offset]
        word_index = int(word_index, 2)

        if block and block.tag == tag and block.valid:
            block.data[word_index] = data
            block.dirty = True
        else:
            if block.dirty:
                self.load_data_from_cache_to_l2_memory(address, block, index)

            self.update_fresh_data_block(block, tag, offset)
            self.load_data_from_l2_memory(address, block, True, word_index, data)

    def load_data_from_cache_to_l2_memory(self, address, block, index):
        for i, word in enumerate(block.data):
            new_address = self.get_word_address(address, index)
            self.l2_memory.write(new_address, block.data[i])

    def load_data_from_l2_memory(self, address, block, write: bool = False, word_index: int = 0, data: str = None):
        for i in range(self.number_of_words_in_block):
            if write and i == word_index:
                block.data[i] = data
                continue
            new_address = self.get_word_address(address, i)
            block.data[i] = self.l2_memory.read(new_address)

    @staticmethod
    def update_fresh_data_block(block, tag, offset):
        block.tag = tag
        block.offset = offset
        block.valid = True
        block.dirty = False

    def get_index(self, address):
        binary_address = convert_to_32_bit(address)
        index = binary_address[-(self.total_offset + self.size_index):-self.total_offset]
        return index

    def get_cache_block(self, address):
        index = self.get_index(address)
        position_in_cache = self.memory.get(index)

        return position_in_cache

    def block_is_dirty(self, address):
        block = self.get_cache_block(address)
        if not block:
            return False
        return block.dirty

    def get_word_address(self, address, index) -> str:
        binary_address = convert_to_32_bit(address)
        new_address = binary_address[:-self.total_offset]
        new_address += convert_to_2_bit(index)
        new_address += binary_address[-self.size_byte_offset:]

        return new_address


class Block:
    def __init__(self):
        self.offset: str = ""  # offset of 4 bits
        self.tag: str = ""  # tag to identify data on address
        self.data: List[str] = ['', '', '', '']  # data saved in the address (4 words)
        self.dirty: bool = False  # if the block was already written
        self.valid: bool = False
