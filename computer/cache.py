from typing import Dict


class Cache:
    def __init__(self):
        self.memory: Dict[str, Block]


class Block:
    def __init__(self):
        self.tag: str
        self.data: str
