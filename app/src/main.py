from onos import Network

# Developer
ip = "192.168.56.105"
DT = Network(ip=ip)
DT.setup()
print(DT.model_dump_json(indent=1))
