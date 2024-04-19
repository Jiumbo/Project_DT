from pydantic import BaseModel, Field
from typing import List, ClassVar
from onos.cluster import Cluster


class Clusters(BaseModel):
    clusters: List[Cluster]
    param: ClassVar[str] = "topology/clusters"
