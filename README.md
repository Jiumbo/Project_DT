# OnosDT

OnosDT is a Digital Twin for Open Network Operating System (ONOS) SDN Controller

## Create Virtual Environment

```bash
py.exe -m venv venv
```
## Activate Virtual Environment (Windows)

```bash
./venv/Scripts/Activate.ps1
```

## Installation
After activate the Virtual Enviroment

```bash
pip install -r requirements.txt
```

## Start Server

```bash
cd ./server/src
py.exe main.py --ip {Onos host Ip}
```

