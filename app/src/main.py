from onos.network import Network
from flaskr.app import app


def main():
    # Developer
    ip = "192.168.56.105"
    DT = Network(ip=ip)


if __name__ == "__main__":
    # main()
    app.run(debug=True)
