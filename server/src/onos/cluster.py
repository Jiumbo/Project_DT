from pydantic import BaseModel, ValidationError
from typing import List, ClassVar
from onos.request_handler import RequestHandler
from onos.device import Device
from onos.host import Host
from onos import logger


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

    def set_devices(self, requester: RequestHandler) -> bool:
        try:
            response = requester.get_request(
                Cluster.param_cluster_id.format(cluster_id=self.id)
            )
            devices_id = response["devices"]
            for device_id in devices_id:
                response = requester.get_request(
                    Cluster.param_device_id.format(device_id=device_id)
                )
                self.devices.append(Device(**response))
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def set_hosts(self, requester: RequestHandler) -> bool:
        try:
            response = requester.get_request(param=Cluster.param_hosts)
            for host in response["hosts"]:
                element = Host(**host)
                for device in self.devices:
                    for location in element.locations:
                        if location.elementId == device.id:
                            device.add_host(host=element)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def set_device_flows(self, requester: RequestHandler):
        for device in self.devices:
            device.set_flows(requester=requester)

    def set_device_flows_table(self, requester: RequestHandler):
        for device in self.devices:
            device.set_flows_table(requester=requester)

    def set_device_port_statistics(self, requester: RequestHandler):
        for device in self.devices:
            device.set_statistics(requester=requester)

    def set_device_port_delta_statistics(self, requester: RequestHandler):
        for device in self.devices:
            device.set_delta_statistics(requester=requester)

    def get_device_by_id(self, device_id: str) -> Device:
        for device in self.devices:
            if device.id == device_id:
                return device

    def get_last_update(self) -> list:
        datetime = []
        for device in self.devices:
            datetime.append(device.lastUpdate)
        return datetime
