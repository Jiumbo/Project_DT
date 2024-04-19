from pydantic import BaseModel
from typing import List
from onos.host_location import HostLocation


class Host(BaseModel):
    id: str
    mac: str
    vlan: str
    innerVlan: str
    outerTpid: str
    configured: bool
    ipAddresses: List
    locations: List[HostLocation]
