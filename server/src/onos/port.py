from pydantic import BaseModel, ValidationError
from typing import ClassVar, Optional
from onos.port_annotations import PortAnnotations
from onos.statistic import Statistics
from onos.request_handler import RequestHandler
from onos import logger


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
    statistics: Optional[Statistics] = None
    delta_statistics: Optional[Statistics] = None

    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)

    def set_statistics(self, device_id: str, requester: RequestHandler) -> bool:
        try:
            if self.port != "local":
                response = requester.get_request(
                    param=Port.param_statistics.format(
                        device_id=device_id, port_id=self.port
                    )
                )
                response = response["statistics"][0]["ports"][0]
                self.statistics = Statistics(**response)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def set_delta_statistics(self, device_id: str, requester: RequestHandler) -> bool:
        try:
            if self.port != "local":
                response = requester.get_request(
                    param=Port.param_delta_statisctics.format(
                        device_id=device_id, port_id=self.port
                    )
                )
                response = response["statistics"][0]["ports"][0]
                self.delta_statistics = Statistics(**response)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
