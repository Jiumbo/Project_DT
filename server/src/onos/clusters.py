from pydantic import BaseModel, Field
from typing import List, ClassVar
from onos.cluster import Cluster
from onos.request_handler import RequestHandler
from itertools import chain


class Clusters(BaseModel):
    clusters: List[Cluster]
    param: ClassVar[str] = "topology/clusters"

    def get_cluster_by_id(self, cluster_id: int) -> Cluster:
        for cluster in self.clusters:
            if cluster.id == cluster_id:
                return cluster

    def set_devices(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_devices(requester=requester)

    def set_devices_flow(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_device_flows(requester=requester)

    def set_devices_flows_table(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_device_flows_table(requester=requester)

    def set_devices_port_statistics(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_device_port_statistics(requester=requester)

    def set_devices_port_delta_statistics(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_device_port_delta_statistics(requester=requester)

    def set_device_hosts(self, requester: RequestHandler):
        for cluster in self.clusters:
            cluster.set_hosts(requester=requester)

    def get_last_update(self):
        datetime = []
        for cluster in self.clusters:
            datetime.append(cluster.get_last_update())
        return list(chain.from_iterable(datetime))
