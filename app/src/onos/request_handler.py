import requests


# Handle the request to the Onos API
"""Handle the Onos API requests from the system"""


class RequestHandler:

    url = "http://{ip}:8181/onos/v1/"
    test_param = "docs/apis"
    user = "onos"
    password = "rocks"
    is_instantiated = False

    def __init__(self, ip: str) -> None:
        if not RequestHandler.is_instantiated:  # Singleton pattern
            RequestHandler.url = RequestHandler.url.format(ip=ip)
            RequestHandler.is_instantiated = True

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
    def test_connection(ip: str) -> bool:
        if not RequestHandler.is_instantiated:
            RequestHandler.url = RequestHandler.url.format(ip=ip)
            RequestHandler.get_request(param=RequestHandler.test_param)
            return True
