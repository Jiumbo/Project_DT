from pydantic import BaseModel, ValidationError
from typing import ClassVar
from onos.port_annotations import PortAnnotations
from onos.statistic import Statistics
from onos.request_handler import RequestHandler


class Port(BaseModel):
    param_statistics: ClassVar[str] = "statistics/ports/{device_id}/{port_id}"
    param_delta_statisctics: ClassVar[str] = (
        "statistics/delta/ports/{device_id}/{port_id}"
    )
    element: str
    port: str | int
    isEnabled: bool
    type: str
    portSpeed: int
    annotations: PortAnnotations
    statistics: Statistics = None
    delta_statistics: Statistics = None

    def set_statistics(self, device_id: str) -> bool:
        try:
            if self.port != "local":
                response = RequestHandler.get_request(
                    param=Port.param_statistics.format(
                        device_id=device_id, port_id=self.port
                    )
                )
                response = response["statistics"][0]["ports"][0]
                self.statistics = Statistics(**response)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def set_delta_statistics(self, device_id: str) -> bool:
        try:
            if self.port != "local":
                response = RequestHandler.get_request(
                    param=Port.param_delta_statisctics.format(
                        device_id=device_id, port_id=self.port
                    )
                )
                response = response["statistics"][0]["ports"][0]
                self.delta_statistics = Statistics(**response)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
