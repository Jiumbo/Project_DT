from pydantic import BaseModel


class Memory(BaseModel):
    current: int
    max: int
    committed: int
