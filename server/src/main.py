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
        await asyncio.sleep(60)


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
    return service.blockchain.model_dump(include={"records"})


@app.get("/{record_id}/clusters")
async def get_clusters(record_id: int):
    network = get_network(record_id=record_id)
    clusters = network.clusters.model_dump(exclude={"param"})
    for cluster in clusters.get("clusters"):
        cluster.pop("devices")
    return clusters


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


@app.get("/{record_id}/{cluster_id}/{device_id}/flows")
async def get_device_flows(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"flows"})


@app.get("/{record_id}/{cluster_id}/{device_id}/ports")
async def get_device_ports(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"ports"})


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


@app.get("/{record_id}/{cluster_id}/{device_id}/tables")
async def get_device_tables(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"tables"})


@app.get("/{record_id}/{cluster_id}/{device_id}/hosts")
async def get_device_hosts(record_id: int, cluster_id: int, device_id: str):
    network = get_network(record_id=record_id)
    device = network.clusters.get_cluster_by_id(cluster_id=cluster_id).get_device_by_id(
        device_id=device_id
    )
    return device.model_dump(include={"hosts"})


@app.get("/{record_id}/metrics")
async def get_metrics(record_id: int):
    network = get_network(record_id=record_id)
    return network.metrics.model_dump()


@app.get("/{record_id}/system")
async def get_system(record_id: int):
    network = get_network(record_id=record_id)
    return network.system.model_dump()


@app.get("/metrics")
async def get_all_metrics():
    metrics_list = []
    chain = service.blockchain.get_chain().copy()
    chain.pop(0)
    for block in chain:
        network = get_network(block.id)
        metrics_list.append(network.metrics.model_dump())
    return metrics_list


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=False)
