# Il blocco ha come attributi :
# Data, Timestamp, Nonce (TTL del nodo in vita di più tempo) Proof of Trustness
# Il suo hash e l'hash del blocco precedente
# Il suo hash è formato dall'enocode in sha256 di : timestamp, data,
# nonce , hash blocco precedente
from pydantic import BaseModel
from typing import Optional
from hashlib import sha256
from datetime import datetime

class Block(BaseModel):
    id: int
    timestamp: datetime
    data: str
    nonce: int
    previous_hash: str | None
    hash: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hash = self.__compute_hash()

    def __compute_hash(self):
        to_hash = f"{self.timestamp}{self.data}{self.nonce}{self.previous_hash}"
        return sha256(to_hash.encode("utf-8")).hexdigest()
