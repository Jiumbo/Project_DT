import requests


# Handle the request to the Onos API
"""Handle the Onos API requests from the system"""


class RequestHandler:

    url = "http://{ip}:8181/onos/v1/"
    test_param = "docs/apis"
    user = "onos"
    password = "rocks"
    instantiated = False

    def __init__(self, ip: str) -> None:
        # self.url = self.url.format(ip=ip)
        if not RequestHandler.instantiated:  # Singleton pattern
            RequestHandler.url = RequestHandler.url.format(ip=ip)
            RequestHandler.instantiated = True

    @staticmethod
    def get_request(param: str) -> dict:
        print(RequestHandler.url + param)
        res = requests.get(
            url=RequestHandler.url + param,
            auth=(RequestHandler.user, RequestHandler.password),
        )
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception

    @staticmethod
    def get_url():
        print(RequestHandler.url)

    @staticmethod
    def test_connection() -> bool:
        res = requests.get(
            url=RequestHandler.url + RequestHandler.test_param,
            auth=(RequestHandler.user, RequestHandler.password),
        )
        if res.status_code == 200:
            return True
        else:
            return False
