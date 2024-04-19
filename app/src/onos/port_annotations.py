from pydantic import BaseModel


class PortAnnotations(BaseModel):
    adminState: str
    portMac: str
    portName: str
