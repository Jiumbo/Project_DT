from pydantic import BaseModel, Field
from typing import List, ClassVar
from onos.cluster import Cluster


class Clusters(BaseModel):
    clusters: List[Cluster]
    param: ClassVar[str] = "topology/clusters"

    def get_clusters_by_id(self, cluster_id: int) -> Cluster:
        for cluster in self.clusters:
            if cluster.id == cluster_id:
                return cluster
