from pydantic import BaseModel
from typing import ClassVar
from onos.memory import Memory
from onos.thread import Thread


class System(BaseModel):
    param: ClassVar[str] = "system"
    node: str
    version: str
    clusterId: str
    nodes: int
    devices: int
    links: int
    hosts: int
    sccs: int
    flows: int
    intents: int
    mem: Memory
    threads: Thread
