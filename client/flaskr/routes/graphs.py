from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from routes import db
from requests import get
from routes.user import get_user_address
import plotly.graph_objs as go
import plotly.io as pio

graph_bp = Blueprint("graph", __name__)


@graph_bp.route("/metrics-graph")
def metrics_graph():
    address = get_user_address()
    response = get("http://{address}/metrics".format(address=address))
    if response.status_code == 200:
        metrics_list = response.json()
        line_fig_html = build_metrics_graph(metrics_list=metrics_list)
        return render_template("metrics-graph.html", line_fig_html=line_fig_html)
    return "ciao"


def build_metrics_graph(metrics_list: list):
    times = list(range(1, len(metrics_list)))
    mean_rates = [metrics["mean_rate"] for metrics in metrics_list]
    rate_1_min = [metrics["rate_1_min"] for metrics in metrics_list]
    rate_5_min = [metrics["rate_5_min"] for metrics in metrics_list]
    rate_15_min = [metrics["rate_15_min"] for metrics in metrics_list]
    rate_traces = [
        go.Scatter(x=times, y=mean_rates, mode="lines+markers", name="Mean Rate"),
        go.Scatter(x=times, y=rate_1_min, mode="lines+markers", name="Rate 1 min"),
        go.Scatter(x=times, y=rate_5_min, mode="lines+markers", name="Rate 5 min"),
        go.Scatter(x=times, y=rate_15_min, mode="lines+markers", name="Rate 15 min"),
    ]
    line_layout = go.Layout(
        title="Rates Over Time",
        xaxis=dict(title="Time Points"),
        yaxis=dict(title="Rates"),
    )
    line_fig = go.Figure(data=rate_traces, layout=line_layout)
    return pio.to_html(line_fig, full_html=False)
