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
    # asyncio.create_task(save_record()) #Per non avviare le VM
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
Esempio risposta : Get Device Ports (Sto valutando se tenere o meno le statistiche o farle a parte)
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
            "statistics": null,
            "delta_statistics": null,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
