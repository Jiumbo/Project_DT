from APIservice import APIService
from fastapi import FastAPI
from argparse import ArgumentParser
from contextlib import asynccontextmanager
import asyncio
from zlib import decompress
from base64 import b64decode
import json
from onos.network import Network

service: APIService = None


# Used to pass the IP of the ONOS host when the API start
def parse_args() -> str:
    parser = ArgumentParser()
    parser.add_argument("--ip", type=str, help="Onos host IP")
    return parser.parse_args()


# The rutine to save the staus of the Network
async def save_record():
    while True:
        service.mine_block()
        await asyncio.sleep(300)


def get_network(record_id: int):
    data = service.blockchain.get_block(block_id=record_id)  # Encoded data
    data = b64decode(data)  # Decoded data
    data = decompress(data).decode()  # Decompressed data
    return Network(**json.loads(data))


# The function to define the "startup" and "shoutdown" event of the API
@asynccontextmanager
async def lifespan(app: FastAPI):
    ip = parse_args().ip
    global service
    service = APIService(ip=ip)
    # asyncio.create_task(save_record())  # Per non avviare le VM
    yield
    service.save_blockchain()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get("/records")
async def get_records():
    return service.blockchain.model_dump(include={"chain"})


""" 
Esempio risposta : Get Clusters
{
    "clusters": [
        {"id": 0, "deviceCount": 3, "linkCount": 4, "root": "of:0000000000000001"}
    ]
} """


@app.get("/{record_id}/clusters")
async def get_clusters(record_id: int):
    data = service.blockchain.get_block(block_id=record_id)  # Encoded data
    data = b64decode(data)  # Decoded data
    data = decompress(data).decode()  # Decompressed data
    network = Network(**json.loads(data))
    clusters = network.clusters.model_dump(exclude={"param"})
    for cluster in clusters.get("clusters"):
        cluster.pop("devices")
    return clusters


""" 
Esempio risposta : Get Cluster Devices
{
    "devices": [
        {
            "id": "of:0000000000000003",
            "type": "SWITCH",
            "available": true,
            "role": "MASTER",
            "mfr": "Nicira, Inc.",
            "hw": "Open vSwitch",
            "sw": "2.13.1",
            "serial": "None",
            "driver": "ovs",
            "chassisId": 3,
            "lastUpdate": 1716729624293,
            "humanReadableLastUpdate": "connected 1h27m ago",
            "annotations": {
                "channelId": "192.168.56.102:48694",
                "managementAddress": "192.168.56.102",
                "protocol": "OF_14",
            },
        }
    ]
} """


@app.get("/{record_id}/{cluster_id}/devices")
async def get_cluster_devices(record_id: int, cluster_id: int):
    network = get_network(record_id=record_id)
    cluster = network.clusters.get_cluster_by_id(cluster_id=cluster_id)
    devices = cluster.model_dump(include={"devices"})
    for device in devices.get("devices"):
        device.pop("ports")
        device.pop("flows")
        device.pop("hosts")
        device.pop("tables")
    return devices


""" 
Esempio risposta : Get Device Flows
{
    "flows": [
        {
            "id": "281476156249461",
            "tableId": "0",
            "appId": "org.onosproject.core",
            "groupId": 0,
            "priority": 40000,
            "timeout": 0,
            "isPermanent": true,
            "deviceId": "of:0000000000000003",
            "state": "ADDED",
            "life": 5275,
            "packets": 1642,
            "bytes": 228238,
            "liveType": "UNKNOWN",
            "lastSeen": 1716734900521,
            "treatment": {
                "instructions": [{"type": "OUTPUT", "port": "CONTROLLER"}],
                "clearDeferred": true,
                "deferred": [],
            },
            "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x8942"}]},
        }
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/flows")
async def get_device_flows(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"flows"})


""" 
Esempio risposta : Get Device Ports
{
    "ports": [
        {
            "element": "of:0000000000000003",
            "port": "local",
            "isEnabled": false,
            "type": "copper",
            "portSpeed": 0,
            "annotations": {
                "adminState": "disabled",
                "portMac": "5a:64:38:ca:4c:47",
                "portName": "s3",
            },
        }
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/ports")
async def get_device_ports(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"ports"})


""" 
Esempio risposta : Get Device Ports Statistics
{
    "ports": [
        {
            "port": "1",
            "isEnabled": true,
            "portSpeed": 10000,
            "statistics": {
                "packetsReceived": 3302,
                "packetsSent": 3301,
                "bytesReceived": 457680,
                "bytesSent": 457638,
                "packetsRxDropped": 0,
                "packetsTxDropped": 0,
                "packetsRxErrors": 0,
                "packetsTxErrors": 0,
                "durationSec": 5097,
            },
        },
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/ports/statistics")
async def get_device_ports_statistics(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    ports = device.model_dump(include={"ports"})
    for port in ports.get("ports"):
        port.pop("element")
        port.pop("type")
        port.pop("annotations")
        port.pop("delta_statistics")
    return ports


""" 
Esempio risposta : Get Device Ports Delta Statistics
{
    "ports": [
        {
            "port": "1",
            "isEnabled": true,
            "portSpeed": 10000,
            "delta_statistics": {
                "packetsReceived": 2,
                "packetsSent": 2,
                "bytesReceived": 278,
                "bytesSent": 278,
                "packetsRxDropped": 0,
                "packetsTxDropped": 0,
                "packetsRxErrors": 0,
                "packetsTxErrors": 0,
                "durationSec": 4,
            },
        },
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/ports/delta_statistics")
async def get_device_ports_delta_statistics(
    record_id: int, cluster_id: int, device_id: str
):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    ports = device.model_dump(include={"ports"})
    for port in ports.get("ports"):
        port.pop("element")
        port.pop("type")
        port.pop("annotations")
        port.pop("statistics")
    return ports


""" 
Esempio risposta : Get Device Tables
{
    "tables": [
        {
            "tableId": "0",
            "activeEntries": 4,
            "packetsLookedUp": 3326,
            "packetsMatched": 3326,
        }
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/tables")
async def get_device_tables(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"tables"})


""" 
Esempio risposta : Get Device Hosts
{
    "hosts": [
        {
            "id": "00:00:00:00:00:02/None",
            "mac": "00:00:00:00:00:02",
            "vlan": "None",
            "innerVlan": "None",
            "outerTpid": "unknown",
            "configured": false,
            "ipAddresses": ["10.0.0.2"],
            "locations": [{"elementId": "of:0000000000000002", "port": "2"}],
        }
    ]
} """


@app.get("/{record_id}/{cluster_id}/{device_id}/hosts")
async def get_device_hosts(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"hosts"})


""" 
Esempio risposta : Get Metrics
{
  "counter": 3,
  "mean_rate": 0.0005674165815012536,
  "rate_1_min": 3.157016537695781e-40,
  "rate_5_min": 2.2910853364402713e-10,
  "rate_15_min": 0.000009467268992346153,
  "mean": 37,
  "min": 9,
  "max": 59,
  "stddev": 25
} """


@app.get("/{record_id}/metrics")
async def get_metrics(record_id: int):
    network = get_network(record_id=record_id)
    return network.metrics.model_dump()


"""
Esempio risposta : Get System
{
  "node": "192.168.56.105",
  "version": "2.0.0",
  "clusterId": "default",
  "nodes": 1,
  "devices": 3,
  "links": 4,
  "hosts": 4,
  "sccs": 1,
  "flows": 12,
  "intents": 0,
  "mem": {
    "current": 247830968,
    "max": 1116733440,
    "committed": 403701760
  },
  "threads": {
    "live": 372,
    "daemon": 354,
    "peak": 374
  }
}
"""


@app.get("/{record_id}/system")
async def get_system(record_id: int):
    network = get_network(record_id=record_id)
    return network.system.model_dump()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
