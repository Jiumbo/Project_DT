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

# The function to define the "startup" and "shoutdown" event of the API
@asynccontextmanager
async def lifespan(app: FastAPI):
    ip = parse_args().ip
    global service
    service = APIService(ip=ip)
    asyncio.create_task(save_record())
    yield
    service.save_blockchain()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get("/records")
async def get_records():
    return service.blockchain.model_dump(include={"chain"})


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=False)
