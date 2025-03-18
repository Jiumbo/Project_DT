from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from routes import db
from requests import get
from datetime import datetime

user_bp = Blueprint("user", __name__)


def get_user_address(): 
    user_doc = db.collection("users").document(session.get("user")).get()
    return user_doc.to_dict().get("address")


@user_bp.route("/dashboard")
def dashboard():
    if session.get("user"):
        return render_template("user-dashboard.html")
    else:
        return redirect(url_for("login.login"))


@user_bp.route("/records")
def records():
    address = get_user_address()
    response = get("http://{address}/records".format(address=address))
    if response.status_code == 200:
        data = response.json().get("records")  # chain -> records
        # for item in data:
        #   item["timestamp"] = datetime.fromtimestamp(item.get("timestamp"))
        # data.pop(0)
        return render_template("records.html", data=data)


@user_bp.route("/clusters")
def clusters():
    address = get_user_address()
    record_id = request.args.get("record-id")
    response = get(
        "http://{address}/{record_id}/clusters".format(
            address=address, record_id=record_id
        )
    )
    if response.status_code == 200:
        data = response.json().get("clusters")
        return render_template("clusters.html", data=data, record_id=record_id)


@user_bp.route("/devices")
def devices():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    print(record_id)
    print(cluster_id)
    response = get(
        "http://{address}/{record_id}/{cluster_id}/devices".format(
            address=address, record_id=record_id, cluster_id=cluster_id
        )
    )
    if response.status_code == 200:
        data = response.json().get("devices")
        return render_template(
            "devices.html", data=data, record_id=record_id, cluster_id=cluster_id
        )
    return {"hello": "hello"}


@user_bp.route("/flows")
def flows():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    device_id = request.args.get("device-id")
    response = get(
        "http://{address}/{record_id}/{cluster_id}/{device_id}/flows".format(
            address=address,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )
    )
    if response.status_code == 200:
        data = response.json().get("flows")
        for item in data:
            item["lastSeen"] = datetime.fromtimestamp((item.get("lastSeen") / 1000))
        return render_template("flows.html", data=data)


@user_bp.route("/hosts")
def hosts():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    device_id = request.args.get("device-id")
    response = get(
        "http://{address}/{record_id}/{cluster_id}/{device_id}/hosts".format(
            address=address,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )
    )
    if response.status_code == 200:
        data = response.json().get("hosts")
        return render_template(
            "hosts.html",
            data=data,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )


@user_bp.route("/statistics")
def statistics():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    device_id = request.args.get("device-id")
    response = get(
        "http://{address}/{record_id}/{cluster_id}/{device_id}/ports/statistics".format(
            address=address,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )
    )
    if response.status_code == 200:
        data = response.json().get("ports")
        for item in data:
            if item.get("port") == "local":
                data.remove(item)
        return render_template("statistics.html", data=data)


@user_bp.route("/ports")
def ports():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    device_id = request.args.get("device-id")
    response = get(
        "http://{address}/{record_id}/{cluster_id}/{device_id}/ports".format(
            address=address,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )
    )
    if response.status_code == 200:
        data = response.json().get("ports")
        return render_template("ports.html", data=data)


@user_bp.route("/tables")
def tables():
    address = get_user_address()
    record_id = request.args.get("record-id")
    cluster_id = request.args.get("cluster-id")
    device_id = request.args.get("device-id")
    response = get(
        "http://{address}/{record_id}/{cluster_id}/{device_id}/tables".format(
            address=address,
            record_id=record_id,
            cluster_id=cluster_id,
            device_id=device_id,
        )
    )
    if response.status_code == 200:
        data = response.json().get("tables")
        return render_template("tables.html", data=data)
