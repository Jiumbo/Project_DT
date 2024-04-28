from pydantic import ValidationError, BaseModel
from typing import Optional
from onos.request_handler import RequestHandler
from onos.clusters import Clusters
from onos.system import System
from onos.metrics import Metrics


class Network(BaseModel):
    system: Optional[System] = None
    metrics: Optional[Metrics] = None
    clusters: Optional[Clusters] = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    """Test the connection, if the connection is enstablished
    the RequestHandler is setted otherwise not."""

    def set_ip_address(self, ip: str) -> bool:
        try:
            if RequestHandler.test_connection(ip=ip):
                print("Connection successful.")
                RequestHandler(ip=ip)
                return True
        except:
            print("Connection failed.")
            return False

    def setup(self) -> bool:
        if RequestHandler.is_instantiated:
            self.system = self.__set_system()
            self.metrics = self.__set_metrics()
            self.clusters = self.__set_clusters()
            return True
        else:
            return False

    def __set_clusters(self) -> Clusters:
        try:
            response = RequestHandler.get_request(param=Clusters.param)
            return Clusters(**response)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def __set_system(self) -> System:
        try:
            response = RequestHandler.get_request(param=System.param)
            return System(**response)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")

    def __set_metrics(self) -> Metrics:
        try:
            response = RequestHandler.get_request(param=Metrics.param)
            response = response["metrics"][0]["metric"]["timer"]
            response["rate_1_min"] = response.pop("1_min_rate")
            response["rate_5_min"] = response.pop("5_min_rate")
            response["rate_15_min"] = response.pop("15_min_rate")
            return Metrics(**response)
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
