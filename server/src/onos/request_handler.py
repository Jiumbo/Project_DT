import requests
from pydantic import BaseModel
from typing import ClassVar
from onos import logger

# Handle the request to the Onos API
"""Handle the Onos API requests from the system"""


class RequestHandler(BaseModel):
    url: ClassVar[str] = "http://{ip}:8181/onos/v1/"
    test_param: ClassVar[str] = "docs/apis"
    user: ClassVar[str] = "onos"
    password: ClassVar[str] = "rocks"
    valid_url: bool = False
    ip: str

    def get_request(self, param: str) -> dict:
        # logger.info(f"Request to URL:{RequestHandler.url.format(ip=self.ip)+param}")
        res = requests.get(
            url=RequestHandler.url.format(ip=self.ip) + param,
            auth=(RequestHandler.user, RequestHandler.password),
            timeout=5,
        )
        if res.status_code == 200:
            self.valid_url = True
            return res.json()

    def test_connection(self) -> bool:
        try:
            logger.info(f"Test connection to IP : {self.ip}")
            self.get_request(param=RequestHandler.test_param)
            logger.info("Connected")
            return True
        except Exception as e:
            self.valid_url = False
            logger.info("Not connection")
            return False
