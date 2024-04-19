from pydantic import BaseModel
from onos.treatment import Treatment
from onos.selector import Selector


class Flow(BaseModel):
    id: int | str
    tableId: int | str
    appId: str
    groupId: int
    priority: int
    timeout: int
    isPermanent: bool
    deviceId: str
    state: str
    life: int
    packets: int
    bytes: int
    liveType: str
    lastSeen: int
    treatment: Treatment
    selector: Selector
