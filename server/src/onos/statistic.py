from pydantic import BaseModel


class Statistics(BaseModel):
    packetsReceived: int
    packetsSent: int
    bytesReceived: int
    bytesSent: int
    packetsRxDropped: int
    packetsTxDropped: int
    packetsRxErrors: int
    packetsTxErrors: int
    durationSec: int
