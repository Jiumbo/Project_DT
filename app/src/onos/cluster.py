from pydantic import BaseModel, ValidationError
from typing import List, ClassVar
from onos.request_handler import RequestHandler
from onos.device import Device
from onos.host import Host


class Cluster(BaseModel):
    param_cluster_id: ClassVar[str] = "topology/clusters/{cluster_id}/devices"
    param_device_id: ClassVar[str] = "devices/{device_id}/ports"
    param_hosts: ClassVar[str] = "hosts"
    id: int
    deviceCount: int
    linkCount: int
    root: str
    devices: List[Device] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__set_devices()
        self.__set_hosts()

    def __set_devices(self) -> bool:
        try:
            response = RequestHandler.get_request(
                Cluster.param_cluster_id.format(cluster_id=self.id)
            )
            devices_id = response["devices"]
            for device_id in devices_id:
                response = RequestHandler.get_request(
                    Cluster.param_device_id.format(device_id=device_id)
                )
                self.devices.append(Device(**response))
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def __set_hosts(self) -> bool:
        try:
            response = RequestHandler.get_request(param=Cluster.param_hosts)
            for host in response["hosts"]:
                element = Host(**host)
                for device in self.devices:
                    for location in element.locations:
                        if location.elementId == device.id:
                            device.add_host(host=element)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
