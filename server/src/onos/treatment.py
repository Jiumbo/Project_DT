from pydantic import BaseModel
from typing import List
from onos.instruction import Instruction


class Treatment(BaseModel):
    instructions: List[Instruction]
    clearDeferred: bool
    deferred: List
