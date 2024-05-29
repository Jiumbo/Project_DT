from pydantic import ValidationError, BaseModel
from typing import Optional
from onos.request_handler import RequestHandler
from onos.clusters import Clusters
from onos.system import System
from onos.metrics import Metrics
from onos import logger


class Network(BaseModel):
    system: Optional[System] = None
    metrics: Optional[Metrics] = None
    clusters: Optional[Clusters] = None
    requester: Optional[RequestHandler] = None

    def __init__(self, requester: RequestHandler = None, **kwargs) -> None:
        super().__init__(**kwargs)
        if (
            type(requester) is RequestHandler
        ):  # Used this strategy to load a Network by an old version
            self.requester = requester

    def update(self) -> bool:
        logger.info("Start updating data")
        self.system = self.__set_system()
        self.metrics = self.__set_metrics()
        self.clusters = self.__set_clusters()
        self.clusters.set_devices(requester=self.requester)
        self.clusters.set_devices_flow(requester=self.requester)
        self.clusters.set_devices_flows_table(requester=self.requester)
        self.clusters.set_devices_port_statistics(requester=self.requester)
        self.clusters.set_devices_port_delta_statistics(requester=self.requester)
        self.clusters.set_device_hosts(requester=self.requester)
        logger.info("Finished updating data")

    def __set_clusters(self) -> Clusters:
        try:
            response = self.requester.get_request(param=Clusters.param)
            return Clusters(**response)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def __set_system(self) -> System:
        try:
            response = self.requester.get_request(param=System.param)
            return System(**response)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def __set_metrics(self) -> Metrics:
        try:
            response = self.requester.get_request(param=Metrics.param)
            response = response["metrics"][0]["metric"]["timer"]
            response["rate_1_min"] = response.pop("1_min_rate")
            response["rate_5_min"] = response.pop("5_min_rate")
            response["rate_15_min"] = response.pop("15_min_rate")
            return Metrics(**response)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")

    def get_last_update(self):
        return self.clusters.get_last_update()
