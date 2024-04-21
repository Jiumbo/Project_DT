from pydantic import BaseModel, ValidationError
from typing import List, ClassVar
from onos.request_handler import RequestHandler
from onos.device_annotations import DeviceAnnotations
from onos.port import Port
from onos.flow import Flow
from onos.host import Host
from onos.table import Table


class Device(BaseModel):
    param_flows: ClassVar[str] = "flows/{device_id}"
    param_flows_table: ClassVar[str] = "statistics/flows/tables/{device_id}"
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
    tables: List[Table] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__set_flows()
        self.__set_statistics()
        self.__set_delta_statistics()
        self.__set_flows_table()

    def __set_flows(self) -> bool:
        try:
            response = RequestHandler.get_request(
                param=Device.param_flows.format(device_id=self.id)
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

    def __set_delta_statistics(self) -> bool:
        for port in self.ports:
            port.set_delta_statistics(device_id=self.id)

    def __set_flows_table(self) -> bool:
        try:
            response = RequestHandler.get_request(
                param=Device.param_flows_table.format(device_id=self.id)
            )
            response = response["statistics"][0]["table"]
            tableids = self.__get_tableids_from_flows()
            for tableid in tableids:
                self.tables.append(
                    Table(**response[tableid])
                )  # Get only the active tables
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def __get_tableids_from_flows(self) -> List:
        tableids = []
        for flow in self.flows:
            tableids.append(int(flow.tableId))  # Cast to int becouse the value was str
        return list(set(tableids))  # Remove duplicates from tableIds list

    def update_flows(self) -> bool:
        self.__set_flows()

    def update_statistics(self) -> bool:
        self.__set_statistics()

    def add_host(self, host: Host) -> bool:
        self.hosts.append(host)
