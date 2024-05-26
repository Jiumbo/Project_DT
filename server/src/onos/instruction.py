from pydantic import BaseModel


class Instruction(BaseModel):
    type: str
    port: str
