from pydantic import BaseModel


class DeviceAnnotations(BaseModel):
    channelId: str
    managementAddress: str
    protocol: str
