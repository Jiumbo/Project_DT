from pydantic import BaseModel, ValidationError
from typing import List, ClassVar
from onos.request_handler import RequestHandler
from onos.device_annotations import DeviceAnnotations
from onos.port import Port
from onos.flow import Flow
from onos.host import Host


class Device(BaseModel):
    param: ClassVar[str] = "flows/{device_id}"
    id: str
    type: str
    available: bool
    role: str
    mfr: str
    hw: str
    sw: str
    serial: str
    driver: str
    chassisId: int
    lastUpdate: int
    humanReadableLastUpdate: str
    annotations: DeviceAnnotations
    ports: List[Port]
    flows: List[Flow] = []
    hosts: List[Host] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__set_flows()
        self.__set_statistics()

    def __set_flows(self) -> bool:
        try:
            response = RequestHandler.get_request(
                param=Device.param.format(device_id=self.id)
            )
            self.flows.clear()
            for flow in response["flows"]:
                self.flows.append(Flow(**flow))
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def __set_statistics(self) -> bool:
        for port in self.ports:
            port.set_statistics(device_id=self.id)

    def update_flows(self) -> bool:
        self.__set_flows()

    def update_statistics(self) -> bool:
        self.__set_statistics()

    def add_host(self, host: Host) -> bool:
        self.hosts.append(host)
