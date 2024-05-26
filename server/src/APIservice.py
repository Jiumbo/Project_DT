from onos.network import Network
from onos.request_handler import RequestHandler
from blockchain.blockchain import BlockChain
from os.path import exists
import json
from zlib import decompress, compress
from base64 import b64encode
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class APIService:
    db_path = "./bc.db"

    def __init__(self, ip: str = None) -> None:
        if exists(self.db_path):
            self.blockchain = self.__load_blockchain()
        else:
            self.blockchain = BlockChain()
        self.network = self.__set_network(ip=ip)

    def __load_blockchain(self) -> BlockChain:
        logger.info("Loading previouse BlockChain")
        f = open(self.db_path, "rb")
        blockchain_data = json.loads(decompress(f.read()).decode())
        f.close()
        return BlockChain(**blockchain_data)

    def __set_network(self, ip: str) -> Network:
        requester = RequestHandler(ip=ip)
        if requester.test_connection():
            return Network(requester=requester)
        else:
            raise ConnectionError

    def save_blockchain(self):
        self.blockchain.save()

    def mine_block(self):
        self.network.update()
        self.blockchain.mine_block(
            self.__compress_data(), self.network.get_last_update()
        )

    def __compress_data(self):
        data = compress(self.network.model_dump_json().encode(), 2)
        return b64encode(data).decode()
