from pydantic import BaseModel
from typing import List
from onos.criteria import Criteria


class Selector(BaseModel):
    criteria: List[Criteria]
