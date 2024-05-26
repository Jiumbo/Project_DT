from pydantic import BaseModel
from typing import List, Dict
from blockchain.block import Block
import random
import zlib
from datetime import datetime


class BlockChain(BaseModel):
    chain: List[Block] = []
    chain_dict: Dict[int, Block] = {}

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if not kwargs:
            self.__mine_genesis_block()

    def __mine_genesis_block(self):
        random.seed("Genesis")
        genesis_block = Block(
            id=len(self.chain),
            data="Genesis Block",
            nonce=random.randint(0, 9999),
            timestamp=datetime.now().timestamp(),
            previous_hash=None,
        )
        self.chain.append(genesis_block)

    def mine_block(self, data: str, ttl: List) -> None:
        new_block = Block(
            id=len(self.chain),
            data=data,
            nonce=min(ttl),
            timestamp=datetime.now().timestamp(),
            previous_hash=self.chain[-1].hash,
        )
        self.chain.append(new_block)
        self.chain_dict[new_block.id] = new_block

    def get_chain(self) -> List:
        return self.chain

    def get_block(self, block_id: int) -> str:
        try:
            return self.chain_dict.get(block_id).data
        except AttributeError:
            pass

    def save(self):
        f = open("./bc.db", "wb")
        f.write(zlib.compress(self.model_dump_json().encode(), 2))
        f.close()
