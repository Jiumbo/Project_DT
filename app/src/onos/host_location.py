from pydantic import BaseModel


class HostLocation(BaseModel):
    elementId: str
    port: str | int
